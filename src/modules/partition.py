def getPartitionBytes(sectorData, cnt):
    sectorBytes = str(sectorData[446:512].hex())
    partitionBytes = []

    for i in range(0, 32 * cnt, 32):
        partitionBytes.append(sectorBytes[i:i + 32])
        if int(partitionBytes[-1], 16) == 0:
            partitionBytes.pop()
            return partitionBytes, -1
    
    extension = partitionBytes.pop()[-16:-8]
    nextSectorNum = ''

    for i in range(8, 0, -2):
        nextSectorNum += extension[i-2:i]
    
    return partitionBytes, int(nextSectorNum, 16)