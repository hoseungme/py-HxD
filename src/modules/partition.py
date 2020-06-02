from .byte import reverseBytes

def getPartitionBytes(sectorData, cnt):
    sectorBytes = str(sectorData[446:512].hex())
    partitionBytes = []

    for i in range(0, 32 * cnt, 32):
        partitionBytes.append(sectorBytes[i:i + 32])
        if int(partitionBytes[-1], 16) == 0:
            partitionBytes.pop()
            return partitionBytes, -1
    
    extension = partitionBytes.pop()[-16:-8]
    nextSectorNum = reverseBytes(extension)
    
    return partitionBytes, int(nextSectorNum, 16)

def getPartitionInfos(sectorData):
    partitionInfos = []
    sectorNum = 0
        
    result, nextSectorNum = getPartitionBytes(sectorData[sectorNum:sectorNum + 512], 4)
    partitionInfos.append({
        'sectorNum': sectorNum,
        'bytes': result,
        'next': nextSectorNum
    })
    sectorNum = partitionInfos[0]['next'] * 512

    while nextSectorNum >= 0:
        result, nextSectorNum = getPartitionBytes(sectorData[sectorNum:sectorNum + 512], 2)
        partitionInfos.append({
            'sectorNum': sectorNum // 512,
            'bytes': result,
            'next': nextSectorNum
        })
            
        sectorNum = (partitionInfos[1]['sectorNum'] + nextSectorNum) * 512
    return partitionInfos

def parsePartitionInfos(partitionInfos):
    parsedPartitionInfos = []
    count = 0

    for e in partitionInfos:
        for byte in e['bytes']:
            count += 1
            bootFlag = byte[0:2]
            chsStart = reverseBytes(byte[2:8])
            partitionType = byte[8:10]
            chsEnd = reverseBytes(byte[10:16])
            lbaStart = e['sectorNum'] + int(reverseBytes(byte[16:24]), 16)
            size = int(reverseBytes(byte[24:32]), 16) * 512 // (1024 ** 2)

            parsedPartitionInfos.append({
                'partitionNum': count,
                'byte': byte,
                'bootFlag': bootFlag,
                'chsStart': chsStart,
                'partitionType': partitionType,
                'chsEnd': chsEnd,
                'lbaStart': lbaStart,
                'size': size
            })
    
    return parsedPartitionInfos

def getFATPartitionInfos(sectorData):
    partitionInfos = parsePartitionInfos(getPartitionInfos(sectorData))
    FATPartitionInfos = []

    for e in partitionInfos:
        if e['partitionType'] == '0c':
            FATPartitionInfos.append(e)
    
    return FATPartitionInfos

def parseFATPartitionInfos(sectorData, FATPartitionInfos):
    parsedFATPartitionInfos = []

    for e in FATPartitionInfos:
        partitionNum = e['partitionNum']
        vbrStart = e['lbaStart']
        byte = str(sectorData[vbrStart * 512:(vbrStart * 512) + 512].hex())
        bytePerSector = int(reverseBytes(byte[22:26]), 16)
        sectorPerCluster = int(byte[26:28], 16)
        reservedSecterCount = int(reverseBytes(byte[28:32]), 16)
        totalSector32 = int(reverseBytes(byte[64:72]), 16)
        fatSize32 = int(reverseBytes(byte[72:80]), 16)
        fat1Start = vbrStart + reservedSecterCount
        fat2Start = fat1Start + fatSize32
        rootDirectoryStart = fat2Start + fatSize32

        parsedFATPartitionInfos.append({
            'partitionNum': partitionNum,
            'bytePerSector': bytePerSector,
            'sectorPerCluster': sectorPerCluster,
            'reservedSectorCount': reservedSecterCount,
            'totalSector32': totalSector32,
            'fatSize32': fatSize32,
            'vbrStart': vbrStart,
            'fat1Start': fat1Start,
            'fat2Start': fat2Start,
            'rootDirectoryStart': rootDirectoryStart
        })

    return parsedFATPartitionInfos