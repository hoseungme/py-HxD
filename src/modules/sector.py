import re

def getSectorInfos(sectorData, num):
    indexMaxLen = len(hex(len(sectorData)).split('x')[1])
    sectorInfos = []

    for i in range(num, num + 512, 16):
        index = hex(i).split('x')[1].rjust(indexMaxLen, '0')
        byte = str(sectorData[i:i + 16].hex())
        temp = []
        decodedText = ''

        for j in range(0, len(byte), 2):
            temp.append(byte[j:j + 2])
            decodedText += chr(int(temp[-1], 16))

        for e in re.compile('[^A-Za-z0-9$&+,:;=?@#|\'"<>.^*()%!-]').findall(decodedText):
            decodedText = decodedText.replace(e, '.')

        sectorInfos.append({
            'index': index,
            'bytes': temp,
            'decodedText': decodedText
        })
    
    return sectorInfos