

import requests, os, boto3, json

class ErrorServiceAWSLambda(Exception):
    """ JM 2022-10
        Classe exception lancée lors d'un probleme avec le serviceBD.

        Exemple apel:   try:
                            ...
                            raise ErreurServiceBD("probleme xyz")
                        except ErreurServiceBD as e:
                            print (e.message)
    """
    def __init__(self, message="Error from ServiceAWSLambda", errorType="ErrorServiceAWSLambda"):
        self.message = message
        self.errorType = errorType

    def __str__(self):
        return repr(self.message)


class ServiceUtilAWSLambda():
    """ 2022-10 JM
    Classe qui sert a alimenter function lambda AWS
    PARAM:


    Exemple
"""

    def __init__(self, bucketName, local=False, awsAccesKeyCsvFile=None):



        self.bucketName = bucketName
        self.local = local
        self.awsAccesKeyFile = awsAccesKeyCsvFile


        if local:

            listAccesKey = self.loadAWSAccessKey()
            self.accesKey = listAccesKey[0]
            self.secretAccesKey = listAccesKey[1]


    def loadAWSAccessKey(self):
        ## JM 2022-10
        ## fonction qui ouvre un fichier .csv de cle de securité AWS

        ## return [accessKey, SecretAccesKey]

        if not self.awsAccesKeyFile:
            raise ErrorServiceAWSLambda("unable to load awsAccesKeyFile the path is empty")


        f = open(self.awsAccesKeyFile, "r")
        print(f.readline())
        listFileRead = f.readline().rstrip('\n').split(',')
        # lines = f.read().splitlines()
        f.close()
        #
        # with open(file, readline) as f:
        #
        #     f.read(base64.b64decode(content))
        return listFileRead
    #

    def saveLocalFileInS3Bucket(self, localPathFileName, inRepTmp = False):
        # /tmp/tes.xml   (in cloud
        # pathFileName = "D:\\python\\gitProjet\\python_project\\AWS\\output\\tmp\\tes.xml

        fileName = os.path.basename(localPathFileName)
        # s3 = boto3.resource("s3")

        # listKey = self.loadAWSAccessKey()
        s3 = boto3.resource('s3',
                            aws_access_key_id= self.accesKey,
                            aws_secret_access_key= self.secretAccesKey)

        s3.meta.client.upload_file(localPathFileName, self.bucketName, fileName)
        ## s3.meta.client.upload_file(lambda_path, bucket_name, file_name)

        return {
            'statusCode': 200,
            'body': json.dumps('file is created in: ' + self.bucketName)
        }

    def saveWmsCallToFileInS3(self, call, fileNameExt, type, repTmp = True):
        # param

        #       fileNameExt = outGeo.pdf
        #       type = ext [geojson, xml, pdf, tif, ect]
        #       pathLocal = path to Save file repertiorie on computer, if true the path must be
        #          gaving in path
        #

        response = requests.get(call)
        content = response.content
        if type in ['json', 'geojson', 'xml']:
            content = response.content.decode("utf-8")


        fileToSave = fileNameExt

        if repTmp:
            fileToSave = "/tmp/" + fileNameExt

        import base64
        # data = response.json()["data"]
        with open(fileToSave, 'wb') as f:
            f.write(content)

        s3 = boto3.resource("s3")

        s3.meta.client.upload_file(fileToSave, self.bucketName, fileNameExt)

        print('load to s3')
        return {
            'statusCode': 200,
            'body': json.dumps('file is created in:' + fileToSave)
        }



    def webServiceCall2paramDict(self, call):

        idx = call.find('?')
        serviceAdress = call[0:idx+1]
        stringParam = call[idx+1:]

        listParam = stringParam.split('&')
        dictParam = {}
        for param in listParam:
            paramValue = param.split('=')
            dictParam[paramValue[0]] = paramValue[1]

        return dictParam



    def BBOX2UllrString(self, bboxString):
        # ullr = upper left, lower right

        bboxList = bboxString.split('%2C')
        if len(bboxList) == 0:
            bboxList = bboxString.split(',')

        ullr = "{0},{1},{2},{3}".format(bboxList[0],bboxList[3],bboxList[2],bboxList[1])

        return ullr




if __name__ == '__main__':

    file = "D:\\AWS\\accessKey\\josee666_accessKeys.csv"
    servAws = ServiceUtilAWSLambda(bucketName="josee-bucket3", local=True, awsAccesKeyCsvFile=file)
    # listKey = servAws.loadAWSAccessKey()

    # print('key: ' ,listKey[0] )
    # print('secretKey: ' ,listKey[1] )

    callWfs_penteLidar = "https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=application/pdf&LAYERS=lidar_pentes&CRS=EPSG%3A3857&WIDTH=787&HEIGHT=907&BBOX=-8002058.621487584%2C5967433.537821494%2C-8000178.748323195%2C5969600.049841952"

    # paramDict = servAws.webServiceCall2paramDict(callWfs_penteLidar)
    # ullr = servAws.BBOX2UllrString(paramDict["BBOX"])

    # file2Save = "D:\\python\\gitProjet\\donneeTests\\AWS\\new\\outCallServ.pdf"
    file2Save = "outCallServ.pdf"
    # servAws.wmsCallToFileInS3(call=callWfs_penteLidar, outputFileNameWithExtension=file2Save, type='pdf', pathLocal=True)
    servAws.wmsCallToFileInS3(call=callWfs_penteLidar, outputFileNameWithExtension=file2Save, type='pdf', pathLocal=False)



    print('ici')