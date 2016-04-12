# Eric Walker & Derek Reitz
# ewalke31 & dreitz5
# CSF HW 7

import sys


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
    outputInfo = simulate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                          sys.argv[5], sys.argv[6], inputList)
    output(outputInfo)
    return


# simulates the cache
def simulate(numSets, numBlocks, numBytes, walloc, wtorb, evictMethod, trace):
    outputInfo = [0, 0, 0, 0, 0, 0, 0]
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
    print("Total cycles: " + str(outputInfo[6]))


if __name__ == "__main__":
    main()
