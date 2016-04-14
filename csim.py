# Eric Walker & Derek Reitz
# ewalke31 & dreitz5
# CSF HW 7

import sys
import math
import time


def main():
    if len(sys.argv) != 8:
        print("Improper number of arguments.")
        sys.exit(1)
    if isPowerTwo(int(sys.argv[1])) == 0 or isPowerTwo(int(sys.argv[2])) == 0 \
       or isPowerTwo(int(sys.argv[3])) == 0 or int(sys.argv[3]) < 4:
        print("Invalid cache setup size arguments.")
        sys.exit(1)
    if (int(sys.argv[4]) != 0 and int(sys.argv[4]) != 1) or \
       (int(sys.argv[5]) != 0 and int(sys.argv[5]) != 1) or \
       (int(sys.argv[6]) != 0 and int(sys.argv[6]) != 1) or \
       (int(sys.argv[4]) == 0 and int(sys.argv[5]) == 0):
        print("Invalid cache design parameters.")
        sys.exit(1)
    inputList = readInput(sys.argv[7])
    outputInfo = simulate(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]),
                          int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]),
                          inputList)
    output(outputInfo)
    return


# simulates the cache
def simulate(numSets, numBlocks, numBytes, walloc, wtorb, evictMethod, trace):
    outputInfo = [0, 0, 0, 0, 0, 0, 0]
    evictSLD = [None]*numSets
    for i in range(numSets):
        blockDict = {}
        for j in range(numBlocks):
            blockDict[j] = float("inf")  # max time value
        evictSLD[i] = blockDict
    validMask = 2
    dirtyMask = 1
    setMask = (numSets - 1) << int(math.log(numBlocks, 2)) \
        << int(math.log(numBytes/4, 2))
    maskSize = int(math.log(numSets, 2) + math.log(numBlocks, 2)
                   + math.log(numBytes/4, 2))
    tagMask = int(math.pow(2, 32 - maskSize) - 1) << maskSize
    cache = [[0]*numBlocks for _ in range(numSets)]
    for line in trace:
        line = line.split()
        binAddr = int(line[1], 16)
        setIndex = (setMask & binAddr) >> int(math.log(numBlocks, 2)) \
            >> int(math.log(numBytes/4, 2))
        if line[0] == 'l':
            outputInfo[0] += 1
            found = False
            numValid = 0
            for block in cache[setIndex]:
                if block & validMask == 2:
                    if((block >> 2) == ((binAddr & tagMask) >> maskSize)):
                        outputInfo[2] += 1
                        outputInfo[6] += 1
                        found = True
                        if evictMethod == 1:  # LRU
                            evictSLD[setIndex][numValid] = time.clock()
                        break
                    numValid += 1
            if not found:
                outputInfo[3] += 1
                outputInfo[6] += (100 * numBytes/4) + 1
                if numValid < numBlocks:
                    cache[setIndex][numValid] = ((binAddr & tagMask)
                                                 >> (maskSize - 2)) + 2
                    evictSLD[setIndex][numValid] = time.clock()
                else:
                    minv = float("inf")
                    mink = None
                    for key, value in evictSLD[setIndex].items():
                        if value < minv:
                            minv = value
                            mink = key
                    if cache[setIndex][mink] & dirtyMask == 1:
                        outputInfo[6] += 100 * numBytes/4
                    cache[setIndex][mink] = ((binAddr & tagMask)
                                             >> (maskSize - 2)) + 2
                    evictSLD[setIndex][mink] = time.clock()
        else:  # if line[0] == 's'
            outputInfo[1] += 1
            numValid = 0
            for block in cache[setIndex]:
                if block & validMask == 2 \
                   and ((block >> 2) == ((binAddr & tagMask) >> maskSize)):
                    outputInfo[4] += 1
                    if wtorb == 0:  # if write back
                        outputInfo[6] += 1
                        if block & dirtyMask == 0:
                            block += 1
                    else:  # if write through
                        outputInfo[6] += 101
                    if evictMethod == 1:  # LRU
                        evictSLD[setIndex][numValid] = time.clock()
                    break
                if block & validMask == 0:  # not valid
                    outputInfo[5] += 1
                    if walloc == 0:  # if not write allocate
                        outputInfo[6] += 100
                    else:  # if write allocate
                        block = ((binAddr & tagMask) >> (maskSize - 2)) + 2
                        outputInfo[6] += 100 * numBytes/4 + 1
                        if wtorb == 1:
                            outputInfo[6] += 100
                    evictSLD[setIndex][numValid] = time.clock()
                    break
                numValid += 1
            if numValid == numBlocks:  # if we need to evict something
                outputInfo[5] += 1
                minv = float("inf")
                mink = None
                for key, value in evictSLD[setIndex].items():
                    if value < minv:
                        minv = value
                        mink = key
                    if cache[setIndex][mink] & dirtyMask == 1:
                        # cost of writing dirty from cache to ram
                        outputInfo[6] += 100 * numBytes/4
                if walloc == 1:
                    # cost of reading from ram to cache
                    outputInfo[6] += 100 * numBytes/4
                    cache[setIndex][mink] = ((binAddr & tagMask)
                                             >> (maskSize - 2)) + 2
                    evictSLD[setIndex][mink] = time.clock()
                outputInfo[6] += 1  # cost of writing to cache
                if wtorb == 1:
                    outputInfo[6] += 100  # cost of writing to ram

    return outputInfo


# checks if a number is a power of two and greater than zero
def isPowerTwo(num):
    return ((num & (num-1)) == 0) and num > 0


# reads in trace input from argument and appends it to list
def readInput(trace):
    inputList = []
    try:
        f = open(trace, 'r')
    except IOError:
        print("Invalid trace file.")
        sys.exit(1)
    for line in f:
        inputList.append(line)
    f.close()
    return inputList


# prints out the required output information
def output(outputInfo):
    print("Total loads: " + str(outputInfo[0]))
    print("Total stores: " + str(outputInfo[1]))
    print("Load hits: " + str(outputInfo[2]))
    print("Load misses: " + str(outputInfo[3]))
    print("Store hits: " + str(outputInfo[4]))
    print("Store misses: " + str(outputInfo[5]))
    print("Total cycles: " + str(int(outputInfo[6])))


if __name__ == "__main__":
    main()
