import os
from msvcrt import getch
from modules.file import getFile
from modules.validators import extValidator, fileValidator, sectorNumValidator
from modules.sector import getSectorInfos
from modules.partition import getPartitionInfos, parsePartitionInfos

f = None
sectorData = ''
index = 0
size = 0

while True:
    print('1. 파일 열기')
    print('2. 섹터 정보')
    print('3. 파티션 정보')
    print('0. 종료', end='\n\n')
    print('메뉴 선택: ', end='')
    menu = input()

    if menu == '1':
        print('\n파일 경로 입력(절대경로): ', end='')

        path = input()

        if extValidator(path):
            f = getFile(path)

            if fileValidator(f):
                sectorData = f.read()
                size = len(sectorData) // 512 - 1
            else:
                print('\n잘못된 경로입니다.')

            print('\n파일 열기 완료')
        else:
            print('\n.dsk 파일이 아닙니다.')
    elif menu == '2':
        if fileValidator(f):
            while True:
                print('\n섹터 번호를 입력하세요 (0 ~ %d, 끝내려면 -1): '%size, end='')
                sectorNum = int(input())

                if sectorNum == -1:
                    print('\n섹터 정보 보기가 종료되었습니다.')
                    break
                
                if sectorNumValidator(sectorNum, size):   
                    os.system('cls')
                    print('%-15s00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F     Decoded text'%'Offset(h)', end='\n\n')

                    for e in getSectorInfos(sectorData, sectorNum * 512):
                        print('%-15s'%e['index'], end='')

                        for byte in e['bytes']:
                            print(byte, end=' ')
                        
                        print('    ' + e['decodedText'])
                else:
                    print('\n섹터 번호가 잘못되었습니다.')
                    break
        else:
            print('\n파일을 열어야 합니다.')
    elif menu == '3':
        os.system('cls')
        count = 0
        print('파티션 정보')

        for e in parsePartitionInfos(getPartitionInfos(sectorData)):
            count += 1
            print('\n\n', end='')
            print('Partition [%d]   '%count, end='')

            for i in range(0, len(e['byte']), 2):
                print(e['byte'][i:i + 2], end=' ')
            
            print('\n\n', end='')
            print('Boot Flag       %s'%e['bootFlag'])
            print('CHS Start       %s'%e['chsStart'])
            print('Type            %s'%e['partitionType'])
            print('CHS End         %s'%e['chsEnd'])
            print('LBA Start       %d'%e['lbaStart'])
            print('size            %d Mbyte'%e['size'])
    elif menu == '0':
        print('\n프로그램을 종료합니다.')
        exit(0)
    
    print('\n계속하려면 아무 키나 누르세요.')
    getch()
    os.system('cls')