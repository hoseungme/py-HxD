from os.path import splitext

def extValidator (path):
    ext = splitext(path)[1]

    if ext == '.dsk':
        return True
    else:
        return False

def fileValidator(f):
    if f is not None:
        return True
    else:
        return False

def sectorNumValidator(num, max):
    if num >= 0 and num <= max:
        return True
    else:
        return False