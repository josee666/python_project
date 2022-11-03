


import requests, os, boto3, json, requests

class ErrorServiceWebService(Exception):
    """ JM 2022-10
        Classe exception lancée lors d'un probleme avec le serviceBD.

        Exemple apel:   try:
                            ...
                            raise ErreurServiceBD("probleme xyz")
                        except ErreurServiceBD as e:
                            print (e.message)
    """
    def __init__(self, message="Error from ServiceWebService", errorType="ErrorServiceWebService"):
        self.message = message
        self.errorType = errorType

    def __str__(self):
        return repr(self.message)


class ServiceUtilWebService():
    """ 2022-10 JM
    Classe qui sert
    PARAM:


    Exemple
"""

    def __init__(self):
        self.adress = ''


    def saveFileFromWMSCall(self, call, pathOutputFile):

        response = requests.get(call)
        content = response.content
        # TODO
        # if type in ['json', 'geojson', 'xml']:
        #     content = response.content.decode("utf-8")


        try:
            os.remove(pathOutputFile)
        except:
            pass


        import base64
        # data = response.json()["data"]
        with open(pathOutputFile, 'wb') as f:
            f.write(content)


    def call2paramDict(self, call):

        idx = call.find('?')
        self.adress = call[0:idx+1]
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


