def getFile(path):
    try:
        f = open(path, mode='rb', buffering=512, encoding=None)
        return f
    except:
        return None