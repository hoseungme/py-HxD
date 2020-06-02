def reverseBytes(byte):
    reversedBytes = ''

    for i in range(8, 0, -2):
        reversedBytes += byte[i-2:i]
    
    return reversedBytes