





def loadAWSAccessKey(fileAwsCsvAccessKey):
    ## JM 2022-10
    ## fonction qui ouvre un fichier .csv de cle de securité AWS

    ## return [accessKey, SecretAccesKey]


    f = open(fileAwsCsvAccessKey, "r")
    print(f.readline())
    listFileRead = f.readline().rstrip('\n').split(',')
    # lines = f.read().splitlines()
    f.close()
    #
    # with open(file, readline) as f:
    #
    #     f.read(base64.b64decode(content))
    return listFileRead


if __name__ == '__main__':

    file = "D:\\AWS\\accessKey\\josee666_accessKeys.csv"
    listKey = loadAWSAccessKey(file)

    print('access: ',listKey[0] )
    print('secret: ',listKey[1] )