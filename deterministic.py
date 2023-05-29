import sys
import statistics

def getMedian(array):
    medianList = []
    for i in range(0, len(array), 5):
        if (i+5) < len(array):
            medianList.append((sorted(array[i:i+5]))[2])
        else:
            temp = array[i:]
            # print("sorted temp = ", sorted(temp))
            medianList.append((sorted(temp))[len(temp) // 2])
    # print("medianList = ", medianList)

    # 2. find the true median of the medians
    if len(medianList) <= 5:
        pivot = (sorted(medianList))[len(medianList) // 2]
        return pivot
    else:
        return getMedian(medianList)


def select(array, k):
    pivot = getMedian(array)

    # 3. use p as a pivot to split the array
    less, greater, equal = [], [], []

    for i in array:
        if i < pivot:
            less.append(i)
        elif i > pivot:
            greater.append(i)
        else:
            equal.append(i)

    # print("less = ", less, "greater = ", greater)
    # 4. recurse
    if (k-1) < len(less):
        return select(less, k)
    elif (k-1) > len(less) + len(equal) - 1:
        return select(greater, k - len(less) - len(equal))
    else:
        return pivot


def main():
    n, k = tuple([int(x) for x in input().split()])
    array = [int(x) for x in input().split()]

    result = select(array, k)
    # print("result = ", result)
    print(result)
    return result





main()