import sys


### defining some global variable
# the base
base = 283
# the prime we use for hashing
prime = 523548799


# helper function for basic hash: hash the char in an alphabet of 62
def mapToAlphabet(x):
    if 57 >= ord(x) >= 48:
        return ord(x) - 48
    elif 90 >= ord(x) >= 65:
        return ord(x) - 55
    else:
        return ord(x) - 61


# helper dict for storing the base with power from 1 to n mod p
def getBase(n):
    result = dict()
    result[0] = 1
    result[1] = base
    for i in range(2, n+1):
        result[i] = result[i-1] * base % prime
    return result


# hashTree: hash the string of alphabet to a single number
def hashTree(array, n):
    def build(u, L, R, tree, n):
        mid = (L + R) // 2
        if (L == R):
            ## reaching a leaf node
            # print(L, R, u)
            tree[u] = (array[L], base)
            # # print(tree[u])
            return

        build(u << 1, L, mid, tree, n)
        build(u << 1 | 1, mid + 1, R, tree, n)

        (leftValue, leftIndex) = tree[u << 1]
        (rightValue, rightIndex) = tree[u << 1 | 1]
        tree[u] = ((leftValue * rightIndex + rightValue) % prime, (leftIndex * rightIndex) % prime)

    tree = [(0, 1) for i in range(4*n)]
    build(1, 0, n - 1, tree, n)
    return tree


# update: update a tree node
def update(u, L, R, i, tree, value):
    mid = (L + R) // 2
    
    if (L == R == i):
        (_, index) = tree[u]
        tree[u] = (value, index)
        return

    # print("entering recursive case, ", u, i, L, R)
    if i >= mid + 1:
        update(u << 1 | 1, mid + 1, R, i, tree, value) # recurse on right child
    else:
        update(u << 1, L, mid, i, tree, value) # recurse on left child

    (leftValue, leftIndex) = tree[u << 1]
    (rightValue, rightIndex) = tree[u << 1 | 1]
    # print("left: ", (leftValue, leftIndex))
    # print("right: ", (rightValue, rightIndex))
    tree[u] = ((leftValue * rightIndex + rightValue) % prime, (leftIndex * rightIndex) % prime)

    return tree



def computeHash(u, i, j, L, R, tree):
    if (i > j):
        return (0, 0)
    mid = (L + R) // 2
    
    if (i <= L and R <= j):
        # print(u, i, j, L, R)
        return tree[u]
    
    if (L == R):
        # print("entering one interval: ", u)
        return tree[u]

    # print("entering recursive case, ", u, i, j, L, R)
    # print(i, mid, j)
    if i >= mid + 1:
        return computeHash(u << 1 | 1, i, j, mid + 1, R, tree) # recurse on right child
    elif j <= mid:
        return computeHash(u << 1, i, j, L, mid, tree) # recurse on left child
    else: # find the correct hash
        # print("fetching value")
        (leftValue, leftIndex) = computeHash(u << 1, i, j, L, mid, tree)
        (rightValue, rightIndex) = computeHash(u << 1 | 1, i, j, mid + 1, R, tree)
        # print("left: ", (leftValue, leftIndex))
        # print("right: ", (rightValue, rightIndex))
        return ((leftValue * rightIndex + rightValue) % prime, (leftIndex * rightIndex) % prime)



# isPalindrome: get sum on interval [l, r)
def isPalindrome(l, r, frontHash, backHash, n):
    if (l >= r):
        return True

    # process the inclusive interval into an open interval
    # # print("frontIndex: ", l, r)
    # # print("backIndex: ", n - r, n - l)


    (frontValue, _) = computeHash(1, l, r, 0, n - 1, frontHash)
    (backValue, _) = computeHash(1, n - r - 1, n - l - 1, 0, n - 1, backHash)
    # print("front value, back value: ", frontValue, backValue)
    return frontValue == backValue

# isJumpPalindrome: get two sum on interval [i, k), 
def isJumpPalindrome(i, k, j, frontHash, backHash, n):
    # print("frontHash", frontHash)
    # print("backHash", backHash)
    if (i >= j): return True

    frontQuery1 = (i, k - 1)
    frontQuery2 = (k+1, j)
    backQuery2 = (n - frontQuery1[1] - 1, n - frontQuery1[0] - 1)
    backQuery1 = (n - frontQuery2[1] - 1, n - frontQuery2[0] - 1)

    # print(i, k, j)
    # print(frontQuery1, frontQuery2)
    # print(backQuery1, backQuery2)

    (frontValue1, _) = computeHash(1, frontQuery1[0], frontQuery1[1], 0, n - 1, frontHash)
    (backValue1, _) = computeHash(1, backQuery1[0], backQuery1[1], 0, n - 1, backHash)
    (frontValue2, _) = computeHash(1, frontQuery2[0], frontQuery2[1], 0, n -1 , frontHash)
    (backValue2, _) = computeHash(1, backQuery2[0], backQuery2[1], 0, n - 1, backHash)

    # print("frontValue1, frontValue2: ", frontValue1, frontValue2)
    # print("backValue1, backValue2: ", backValue1, backValue2)

    baseFront = baseDict[j - k]
    baseBack = baseDict[k - i]

    # print("baseFront, baseBack: ", baseFront, baseBack)

    frontValue = ((frontValue1 * baseFront) % prime + frontValue2) % prime
    backValue = ((backValue1 * baseBack) % prime + backValue2) % prime 

    # print("frontValue, backValue: ", frontValue, backValue)
    return frontValue == backValue



def main():
    # step 0. process read in
    n, k = tuple([int(x) for x in input().split()])
    array = list(map(mapToAlphabet, list(str(input()))))
    reverseArray = list(reversed(array))
    queries = []
    got = 0
    while (got < k):
        queries.append([x for x in input().split()])
        got += 1
    # # print(array)
    # # print(queries)

    global baseDict
    baseDict = getBase(n)

    # step 1. hash the left to right number and right to left number
    frontHash = hashTree(array, n)
    backHash = hashTree(reverseArray, n)
    # print("initialized front hash: ", frontHash)
    # print("initialized back hash: ", backHash)

    result = []

    # step 2. analyze queries
    for query in queries:
        if query[0] == "M":
            # print("\n")
            # print("entering M...")
            i = int(query[1])
            c = mapToAlphabet(query[2])
            # print ("i = ", i, " c = ", c)
            # print("front back index: ", i, n - i - 1)


            frontHash = update(1, 0, n - 1, i, frontHash, c)
            backHash = update(1, 0, n - 1, n - i - 1, backHash, c)

            # print("updated fronHash backHash: ")
            # print(frontHash)
            # print(backHash)
           

        elif query[0] == "Q":
            # print("\n")
            # print("entering Q...")
            i = int(query[1])
            j = int(query[2])
            # print ("i = ", i, " j = ", j)
            if (isPalindrome(i, j, frontHash, backHash, n)): result.append("YES")
            else: result.append("NO")
           

        elif query[0] == "P":
            # # # print("\n")
            # # # print("entering P...")
            i = int(query[1])
            k = int(query[2])
            j = int(query[3])
            if (isJumpPalindrome(i, k, j, frontHash, backHash, n)): result.append("YES")
            else: result.append("NO")
        
        elif query[0] == "C":
            i = int(query[1])
            j = int(query[2])
            # # # print(computeHash(1, i, j, 0, n - 1, frontHash))
            # # print(computeHash(1, n - 1 - j, n - 1 - i, 0, n - 1, backHash))

        else:
            print("invalid query")
        
    for i in result: print(i)
    return result
    

main()