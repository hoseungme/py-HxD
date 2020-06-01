import os
from msvcrt import getch
from modules.file import getFile
from modules.validators import extValidator, fileValidator, sectorNumValidator
from modules.tui import printSectorInfo

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
    menu = int(input())

    if menu == 1:
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
    elif menu == 2:
        if fileValidator(f):
            while True:
                print('\n섹터 번호를 입력하세요 (0 ~ %d, 끝내려면 -1): '%size, end='')
                sectorNum = int(input())

                if sectorNum == -1:
                    print('\n섹터 정보 보기가 종료되었습니다.')
                    break
                
                if sectorNumValidator(sectorNum, size):   
                    os.system('cls')
                    printSectorInfo(sectorData, sectorNum * 512)
                else:
                    print('\n섹터 번호가 잘못되었습니다.')
                    break
        else:
            print('\n파일을 열어야 합니다.')
    elif menu == 0:
        print('\n프로그램을 종료합니다.')
        exit(0)
    
    print('\n계속하려면 아무 키나 누르세요.')
    getch()
    os.system('cls')