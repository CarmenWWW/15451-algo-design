## bsd.py


'''
    splay_tree_starter.py

    This file implements a bottom-up splay tree, a self-balancing binary search
    tree. You can find more information about the data structure and its
    gauranteed time bounds here:

        https://www.cs.cmu.edu/~15451-s22/lectures/lec04-splay.pdf

    Written for the course (15-451 Algorithm Design and Analysis) at Carnegie
    Mellon University.

    Contact: Kunal Joshi <kunalj@andrew.cmu.edu>
    Last updated: 2022-08-29
'''


###############################################################################
# NODE CLASS
###############################################################################

class Node:

    '''
    Node constructor.
        - Gives node an initial given value (`v`).
        - Node is initally isolated; it's connected to no other nodes.
    '''
    def __init__(self, v : int):

        # initialize node value to given value
        self.value = v

        # initialize surrounding nodes to None
        self.left = None
        self.right = None
        self.parent = None

        # define rank as the size of left subtree + size of right subtree + 1
        self.rank = 1

###############################################################################
# SPLAY TREE CLASS
###############################################################################

class SplayTree:

    # -------------------------------------------------------------------------
    # ROTATION
    # -------------------------------------------------------------------------

    '''
    Set `parent`'s left child to `left`, updating `left`'s parent pointer as
    necessary.

    @requires :: `parent` cannot be None
    '''
    def _set_left(self, parent : Node, left : Node) -> None:
        # check precondition
        assert parent != None, "Cannot set the left child of an empty tree"

        # set left child of `parent` to `left` and parent of `left` to `parent`
        parent.left = left
        if (left != None): left.parent = parent
        

    '''
    Set `parent`'s right child to `right`, updating `right`'s parent pointer as
    necessary.

    @requires :: `parent` cannot be None
    '''
    def _set_right(self, parent : Node, right : Node) -> None:
        # check precondition
        assert parent != None, "Cannot set the right child of an empty tree"

        # set left child of `parent` to `right` and parent of `right` to `parent`
        parent.right = right
        if (right != None): right.parent = parent


    '''
    Swap `old` child of `parent` for `new` child/

    @requires :: `old` cannot be None
                    AND `new` cannot be None
                    AND if `parent` is not None, `old` is a child of `parent`
    '''
    def _swap_child(self, parent : Node, old : Node, new : Node) -> None:
        # check preconditions
        assert old != None, "Cannot swap for an empty old child"
        assert new != None, "Cannot swap for an empty new child"

        # determine if old is the left or right child
        # then, swap children and set parent pointer as necessary
        new.parent = parent
        if (parent == None): self.root = new
        elif (parent.left == old): parent.left = new
        elif (parent.right == old): parent.right = new
        else: assert False, "Can only swap for existing child"

    '''
    Perform a left rotation about the node `x`.

                  z                                        z
                 /                                        /
                y                                        x
               / \                                      / \
              x   C       left rotation about x        A   y
             / \       <===========================       / \
            A   B                                        B   C

    @requires :: `x` cannot be None AND `x` must have a non-None right child
    '''
    def _rotate_left(self, x : Node) -> None:
        # check preconditions
        assert x != None, "Cannot rotate an empty tree"
        assert x.right != None, "Cannot rotate left with no right child"

        # store all subtrees from diagram
        y = x.right
        z = x.parent
        A = x.left
        B = y.left
        C = y.right

        # perform rotation by swapping subtrees
        self._swap_child(z, x, y)
        self._set_right(y, C)
        self._set_left(y, x)
        self._set_right(x, B)
        self._set_left(x, A)

        # calculate rank
        x.rank = 1
        if A:
            x.rank += A.rank
        if B:
            x.rank += B.rank

        y.rank = x.rank + 1
        if C:
            y.rank += C.rank


    '''
    Perform a right rotation about the node `y`.

                  z                                        z
                 /       right rotation about y           /
                y      ===========================>      x
               / \                                      / \
              x   C                                    A   y
             / \                                          / \
            A   B                                        B   C

    @requires :: `y` cannot be None AND `y` must have a non-None left child
    '''
    def _rotate_right(self, y : Node) -> None:
        # check preconditions
        assert y != None, "Cannot rotate an empty tree"
        assert y.left != None, "Cannot rotate left with no left child"

        # store all subtrees from diagram
        x = y.left
        z = y.parent
        A = x.left
        B = x.right
        C = y.right

        # perform rotation by swapping subtrees
        self._swap_child(z, y, x)
        self._set_left(x, A)
        self._set_right(x, y)
        self._set_left(y, B)
        self._set_right(y, C)

        # calculate rank
        y.rank = 1
        if B:
            y.rank += B.rank
        if C:
            y.rank += C.rank

        x.rank = 1 + y.rank
        if A:
            x.rank += A.rank

    # -------------------------------------------------------------------------
    # SPLAYING
    # -------------------------------------------------------------------------

    '''
    Splay `x` one step.

    Splay `x` closer to the root by one step using rotations. Takes into
    consideration parent and grandparent of `x`, if necessary.

    Diagrams of each step are also below.

    @requires :: `x` must be non-None.
    '''
    def _splaystep(self, x : Node) -> None:
        # check precondition
        assert x != None, "Cannot run a splay step on an empty tree"

        # if node at root, return
        y = x.parent
        if (x.parent == None): return

        # get grandparent, if exists
        z = y.parent

        # determine case for splay step
        if (z == None and y.left == x):
            '''
                                           y             x
            Zig (y is the tree root):     /     ====>     \
                                         x                 y
            '''
            self._rotate_right(y)
        elif (z == None and y.right == x):
            '''
                                          y                 x
             Zig (y is the tree root):     \     ====>     /
                                            x             y
            '''
            self._rotate_left(y)
        elif (z.left == y and y.right == x):
            '''
                              z              z
                             /              /             x
             Zig-zag:       y     ====>    x   ====>     / \
                             \            /             y   z
                              x          y
            '''
            self._rotate_left(y)
            self._rotate_right(z)
        elif (z.right == y and y.left == x):
            '''
                            z            z
                             \            \               x
             Zig-zag:         y   ====>    x   ====>     / \
                             /              \           z   y
                            x                y
            '''
            self._rotate_right(y)
            self._rotate_left(z)
        elif (z.left == y and y.left == x):
            '''
                              z                         x
                             /            y              \
             Zig-zig:       y     ====>  / \   ====>      y
                           /            x   z              \
                          x                                 z
            '''
            self._rotate_right(z)
            self._rotate_right(y)
        elif (z.right == y and y.right == x):
            '''
                          z                                 x
                           \              y                /
             Zig-zig:       y     ====>  / \   ====>      y
                             \          z   x            /
                              x                         z
            '''
            self._rotate_left(z)
            self._rotate_left(y)
        else: assert False, "Cannot perform splay step due to invalid tree"

    '''
    Splay `xnode` to top of tree.

    Perform splay steps with respect to `xnode` until it reaches the top of
    the tree.

    @requires :: xnode is not None
    '''
    def _splaynode(self, xnode : Node) -> None:
        # check precondition
        assert xnode != None, "Cannot splay an empty tree"

        # splay until node is on top
        while (xnode.parent != None): self._splaystep(xnode)

    '''
    Splay node with value `x`.

    Splay node with integer value `x` in the tree to the top of the tree. The
    node with value `x` will be the root after this operation.

    This method finds the node with value `x`, and then calls _splaynode on
    this found node.

    @requires :: `x` must correspond to a node in the tree
    '''
    def _splay(self, x : int) -> None:
        # check preconditions
        assert x >= 0 and x < self.n, "Value must correspond to a node in tree"

        # extract correct node pointer and splay
        self._splaynode(self.nodes[x])

    # -------------------------------------------------------------------------
    # CONSTRUCTOR
    # -------------------------------------------------------------------------

    '''
    Tree constructor.

    Builds a linked-list splay tree with the following structure...
                                n
                               /
                             ...
                             /
                            1
    ...where the leaf has value 1 and the root has value `n.`

    @requires :: n >= 0
    '''
    def __init__(self, n : int):
        # check precondition
        assert n >= 0, "Cannot create a splay tree with negative nodes"

        prev = None # previous node
        nodes = [] # list of nodes in tree
        for i in range(0, n):

            # initialize new node (and append to list)
            new_node = Node(i)
            nodes.append(new_node)

            # set relationship between new node and remaining tree
            self._set_left(new_node, prev)
            if prev:
                new_node.rank = 1 + prev.rank
            prev = new_node

        # set instance variables to collected information
        self.root = prev
        self.nodes = nodes
        self.n = len(nodes)

    # -------------------------------------------------------------------------
    # TRAVERSAL / PRINTING
    # -------------------------------------------------------------------------

    '''
    Recursive in-order traversal from `x`.

    Traverses the tree rooted at `x` and adds the nodes to a given array
    `A` via in-order ordering.
    '''
    def _inorder(self, x : Node, A : list) -> None:
        if (x == None): return # if dead-end, return

        # add left, cur, right (in this order)
        self._inorder(x.left, A)
        A.append(x.value)
        self._inorder(x.right, A)

    '''
    Generates a string representing the tree structure using a recursive
    parentheses format...

        root (left-subtree) (right-subtree)

    ...if the root does not have a right subtree, no right parentheses
    are printed.

    This method is not optimal and is meant to be used for debugging.
    '''
    def _tostring(self, x : Node) -> str:

        # bases case
        if (x == None): return ""

        # output string
        out = ""

        # push the root data as character
        out += str(x.value)
        if (x.left == None and x.right == None): return out

        # for left subtree
        out += ('(')
        out += self._tostring(x.left)
        out += (')')

        # only if right child is present to avoid extra parenthesis
        if (x.right != None):
            out += ('(')
            out += self._tostring(x.right)
            out += (')')

        return out

    def __str__(self): return self._tostring(self.root)

###############################################################################
# PUBLIC INTERFACE
###############################################################################

'''
Builds (and returns) a splay tree with node values `1...n`
Returned tree will initally have a linked list structure
'''
def create(n : int) -> SplayTree:
    return SplayTree(n)

'''
Splays node with value `x` to the top of splay tree `T`
'''
def splay(T : SplayTree, x : int) -> None:
    T._splay(x)

'''
Prints the nodes of splay tree `T`.
'''
def print_tree(T : SplayTree) -> None:
    print(T)



n, m = tuple([int(x) for x in input().split()])
tree = create(n)

array = []

for line in range(m):
    array.append(int(input()))

result = []
for i in array:
    # step 1. splay the input node to root
    # step 2. calculate rank
    splay(tree, i)
    # print_tree(tree)
    leftNode = tree.root.left
    rightNode = tree.root.right

    # print("root value:", tree.root.value)
    if leftNode == None and rightNode == None:
        # only element
        result.append(0)
        break

    elif leftNode == None:
        # leftest node
        result.append(0)
        tree.root = rightNode
        tree.root.parent = None

    elif rightNode == None:
        # no need to splay right tree
        result.append(tree.root.left.rank)

        tree.root = leftNode
        tree.root.parent = None

    else:
        result.append(tree.root.left.rank)

        # step 0. erase out the root
        leftNode.parent = None
        rightNode.parent = None
        tree.root = rightNode

        # step 1. splay the right tree
        ## get the rightmost node
        rightmost = rightNode
        while (rightmost.right):
            rightmost = rightmost.right
        
        ## splay the rightmost node to the root
        splay(tree, rightmost.value)

        # step 2. set the left subtree
        tree.root.right = leftNode
        leftNode.parent = tree.root



# print("result = ", result)
for i in result:
    print(i)

