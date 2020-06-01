import re

def printSectorInfo(sectorData, num):
    indexMaxLen = len(hex(len(sectorData)).split('x')[1])
    decodedText = ''
    printCount = 0
    maxCount = 16

    print('%-15s00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F   Decoded text'%'Offset(h)', end='\n\n')
    for i in range(num, num + (16 * 32), 16):
        index = hex(i).split('x')[1].rjust(indexMaxLen, '0')
        byte = str(sectorData[i:i + 16].hex())
        print('%-15s'%index, end='')

        for j in range(0, len(byte), 2):
            print(byte[j:j + 2], end='')
            printCount += 1

            decodedText += chr(int(byte[j:j + 2], 16))

            if printCount == maxCount:
                for e in re.compile('[^A-Za-z0-9$&+,:;=?@#|\'"<>.^*()%!-]').findall(decodedText):
                    decodedText = decodedText.replace(e, '.')

                print('   ' + decodedText)

                decodedText = ''
                maxCount += 16
            else:
                print(' ', end='')