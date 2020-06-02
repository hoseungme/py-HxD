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

    for e in partitionInfos:
        for byte in e['bytes']:
            bootFlag = byte[0:2]
            chsStart = reverseBytes(byte[2:8])
            partitionType = byte[8:10]
            chsEnd = reverseBytes(byte[10:16])
            lbaStart = e['sectorNum'] + int(reverseBytes(byte[16:24]), 16)
            size = int(reverseBytes(byte[24:32]), 16) * 512 // (1024 ** 2)

            parsedPartitionInfos.append({
                'byte': byte,
                'bootFlag': bootFlag,
                'chsStart': chsStart,
                'partitionType': partitionType,
                'chsEnd': chsEnd,
                'lbaStart': lbaStart,
                'size': size
            })
    
    return parsedPartitionInfos