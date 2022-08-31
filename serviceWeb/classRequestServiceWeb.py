import xmltodict
import urllib.parse
import requests
import json
import os


class ErreurServiceWeb(Exception):
    """ JM 2022-04
        Classe exception lance lors d'un probleme avec la class service.
        Exemple apel:   try:
                            ...
                        raise ErreurServiceWeb('probleme ici')
                        except ErreurServiceWeb as e:
                            print (e.message)
    """
    def __init__(self, message=u'Probleme class ServiceWeb', type=u'ErreurService'):
        self.message = message
        self.type = type

    def __str__(self):
        return repr(self.message)



class RequeteServiceWeb():

    """ JM: 2022-04
    class qui apel des service web

    NB: - la reponse d'apel WFS est sauvegardée en fichier geojson pour utilisation dans les SIG par default dans
         C:/Logiciels/temp
        - Pour faire des apel WFS la cocuhe apellée doit avoir cet option.
        - Suite a la construction d'un obj de la classe, un dict nomCouche - listeAttributs est dispo dans le param: dictWfsLayer_name_attributs

    PARM:
        url: url du serviceWeb par default url du serviceWeb de la dif
        repSavOutput: Le path du repertoire ou sera sauvegardé le geojson resultant de la requete lancée. S'il
            n'existe pas il sera cree
        projection: projection souhaité pour fichier output ** doit etre en string avec le EPSG dedans. Ex: 'EPSG:32198'        listWfsLayerName: Une liste des noms de couches dispo en WFS
        dictWfsLayer_name_attributs: Un dictionnaire clé= nomCouche : valeur=List attributs de la couche


    Exemple apel:
        objService = RequeteServiceWeb()
        reponse = objService.getWFSPeuplementFromGeocode('-26282,28+540723,32')
        ## un geojson sera sauvegarder et l'objet reponse contiendra tout les attributs du peup correspondant


    Exemple2:

        objService = RequeteServiceWeb(repSavOutput='C:/Logiciels/temp/josee')
        list_polygon= objService.getWfsFilterLayerWithPropertyEgale(layerName='ca_feux_close_scale',
                    propertyName='exercice', valeurEgaleA='2012')
        ## list_polygon sera une list[] comprenant tous les polygones de feux ayant exercice=2012
        ## Un geojson avec les polygones est creé dans C:/Logiciels/temp/josee


    Exemple3: Voir dictionaire des couches et leur attributs disponibles dans le service en WFS

        objService = RequeteServiceWeb(repSavOutput='C:/Logiciels/temp/josee')
        for item in objService.dictWfsLayer_name_attributs:
            print(item)


    Exemple4: sortir le point de la caserne d'incendie de la ville de Donnaconaà
        objService = RequeteServiceWeb(url='https://geoegl.msp.gouv.qc.ca/ws/igo_gouvouvert.fcgi?', repSavOutput='C:/Logiciels/temp/josee')
        listPoint = objService.getWfsFilterLayerWithPropertyEgale(layerName='CASERNE',
                        propertyName='ville', valeurEgaleA='Donnacona')

    """


    def __init__(self, url='https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?', repSavOutput='C:/Logiciels/temp', projection='EPSG:3857'):

        self.url = url
        self.repSavOutput = repSavOutput

        self.paramBaseWfs = {
            'SERVICE': 'WFS',
            'VERSION': '2.0.0',
            'REQUEST': 'GetFeature',
        }
        self.projection = projection

        self.namespaces = {'http://mapserver.gis.umn.edu/mapserver': None,  # skip this namespace
                           'http://www.opengis.net/gml': None,
                           "http://www.opengis.net/wfs": None,
                           "http://www.opengis.net/ows/1.1": None,
                           "http://www.opengis.net/wfs/2.0": None,
                           "http://www.opengis.net/fes/2.0": None,
                           "http://www.w3.org/2001/XMLSchema-instance": None,
                           "http://www.w3.org/2001/XMLSchema": None,
                           }

        self.listWfsLayerName = []
        self.dictWfsLayer_name_attributs = {}
        self.createRepSauvegardeOutput()
        self.fillListDictWfsLayerName()




    def createRepSauvegardeOutput(self):
        if not os.path.exists(self.repSavOutput):
            os.makedirs(self.repSavOutput)



    #     PARAMSGetFeatureI = {
    #     'SERVICE': 'WMS',
    #     'VERSION': '1.3.0',
    #     'REQUEST': 'GetFeatureInfo',
    #     # 'FORMAT': 'image/png',
    #     'QUERY_LAYERS': 'nord_photo_oblique',
    #     'LAYERS': 'nord_photo_oblique',
    #     # 'DPI': '96',
    #     # 'MAP_RESOLUTION': '96',
    #     # 'FORMAT_OPTIONS': 'dpi:96',
    #     'FILTER': '(<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo matchCase="true"><PropertyName>NOM_PHOTO</PropertyName><Literal>_DDD2941.jpg</Literal></PropertyIsEqualTo></Filter>)',
    #     # 'FILTER': '(%3CFilter%20xmlns%3D%22http%3A%2F%2Fwww.opengis.net%2Fogc%22%3E%3CPropertyIsEqualTo%20matchCase%3D%22true%22%3E%3CPropertyName%3EtypeAppareil%3C%2FPropertyName%3E%3CLiteral%3ERadar%20photo%20fixe%3C%2FLiteral%3E%3C%2FPropertyIsEqualTo%3E%3C%2FFilter%3E)',
    #     # 'INFO_FORMAT': 'text/plain',
    #     # 'INFO_FORMAT': 'application/json', ## non pas dispo pour GetFeatureInfo
    #     # 'INFO_FORMAT': 'application/vnd.ogc.gml',
    #     'OUTPUTFORMAT': 'GEOJSON'
    #     # 'OUTPUTFORMAT': 'GML2'
    #     'FEATURE_COUNT': '5',
    #     'I': '50',
    #     'J': '50',
    #     'CRS': 'EPSG:3857',
    #     # 'STYLES': '',
    #     'WIDTH': '101',
    #     'HEIGHT': '101',
    #     'BBOX': '-7997104.281409148,5677667.427515962,-7750059.805991458,5924711.9029336525'
    # }

    def fillListDictWfsLayerName(self):

        call = "{}request=getcapabilities&service=wfs".format(self.url)
        reponse = requests.get(call)

        dictResponse = xmltodict.parse(reponse.content,process_namespaces=True, namespaces=self.namespaces)
        dictName_title = {}

        for layerDictItems in dictResponse['WFS_Capabilities']['FeatureTypeList']['FeatureType']:
            self.listWfsLayerName.append(layerDictItems['Name'])

            dictName_title[layerDictItems['Name']] = layerDictItems['Title']

        ## POUR CHAQUE COUCHE ALLER CHERCHER LA LISTE D'ATTRIBUT POUR CHAQU'UNE

        for i in self.listWfsLayerName:
            # describeFeatureCall = "{0}SERVICE=WFS&REQUEST=DescribeFeatureType&VERSION=2.0.0&TYPENAME={1}".format(self.url, i)
            # reponse = requests.get(describeFeatureCall)
            # dictDescribeResponse = xmltodict.parse(reponse.content, process_namespaces=True, namespaces=namespaces)
            # listDictAttribut = dictDescribeResponse['schema']['complexType']['complexContent']['extension']['sequence']['element']
            # listAttribut = []
            # for j in listDictAttribut:
            #     listAttribut.append(j['@name'])

            listAttribut = self.getListAttributDescribeFeature(i)
            listAttribut.insert(0, (dictName_title[i]))
            self.dictWfsLayer_name_attributs[i] = listAttribut



    def getListAttributDescribeFeature(self, layerName):

        describeFeatureCall = "{0}SERVICE=WFS&REQUEST=DescribeFeatureType&VERSION=2.0.0&TYPENAME={1}".format(self.url, layerName)
        reponse = requests.get(describeFeatureCall)
        dictDescribeResponse = xmltodict.parse(reponse.content, process_namespaces=True, namespaces=self.namespaces)
        listDictAttribut = dictDescribeResponse['schema']['complexType']['complexContent']['extension']['sequence']['element']
        listAttribut = []
        for j in listDictAttribut:
            listAttribut.append(j['@name'])
        return listAttribut


    def lanceRequete(self, params, outputFormat='GEOJSON', saveReponseGeojson=True):

        reponse = requests.get(self.url, params)

        if reponse.status_code != 200 or 'exception' in reponse.text:
            raise ErreurServiceWeb("un probleme est survenue dans l'apel au service Web\nstatus HTTP requete = {0}\n message erreur = {1}\n\nrequete lancée= {2}"
                                   .format(reponse.status_code, reponse.text, reponse.url))

        if outputFormat == 'GEOJSON':
            # reponse_json = reponse.content.decode('utf8').replace("'", '"')
            reponse_json = json.loads(reponse.content)
            if 'features' in reponse_json:
                if saveReponseGeojson:
                    with open('{}/data.geojson'.format(self.repSavOutput), 'w', encoding='utf-8') as f:
                        json.dump(reponse_json, f, ensure_ascii=False, indent=4)
                return reponse_json['features']

            else:
                return reponse_json

        elif outputFormat == 'GML2':
            print('a faire en gml')
            raise ErreurServiceWeb("la sortie GML2 n'est pas encore fait dans le code voir JM si vous en avez besoin")


    def getWmsFilterLayerWithPropertyEgale(self, layerName, propertyName, valeurEgaleA):
        print('a faire')


    def getWfsFilterLayerWithPropertyEgale(self, layerName, propertyName, valeurEgaleA,
                                           outputFormat='GEOJSON', saveOutputGeojson=True):

        # valeurEncode = urllib.parse.quote(valeurEgaleA) ##JM pas besoin encodage, ce fait automatique dans le request.get()
        params = self.paramBaseWfs
        params['TYPENAMES'] = layerName
        params['OUTPUTFORMAT'] = outputFormat
        params['FILTER'] = '<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo matchCase="true"><PropertyName>{0}</PropertyName><Literal>{1}</Literal></PropertyIsEqualTo></Filter>'.format(propertyName, valeurEgaleA),
        if self.projection != 'EPSG:3857':
            params['SRSNAME'] = self.projection
        return self.lanceRequete(params, outputFormat, saveOutputGeojson) ## donne une liste de feature

    def getWFSPeuplementFromGeocode(self, geocode, outputFormat='GEOJSON'):
        ### focntion qui prend en entré un geocode et retourne les informations du WFS (geometrie + info)


        if outputFormat.upper() == 'GEOJSON' or outputFormat.upper() == 'JSON':
            outputFormat = 'GEOJSON'
        elif outputFormat.upper() == 'GML' or outputFormat == 'GML2':
            outputFormat = 'GML2'
        else:
            raise ErreurServiceWeb('Le type de outputFormat est inconnue. Options possibles : GML2 ou geojson')

        list_feature = self.getWfsFilterLayerWithPropertyEgale(layerName='ori_pee_close_scale', propertyName='geocode',                 valeurEgaleA=geocode, outputFormat=outputFormat)

        return list_feature[0]




if __name__ == "__main__":

    objService = RequeteServiceWeb(repSavOutput='C:/Logiciels/temp/josee')


    # objService = RequeteServiceWeb(url='https://geoegl.msp.gouv.qc.ca/ws/igo_gouvouvert.fcgi?', repSavOutput='C:/Logiciels/temp/josee')
    # listPoint = objService.getWfsFilterLayerWithPropertyEgale(layerName='CASERNE',
    #                 propertyName='ville', valeurEgaleA='Donnacona')

    # objService = RequeteServiceWeb(repSavOutput='C:/Logiciels/temp/josee')
    # reponse = objService.getWFSPeuplementFromGeocode('-26282,28+540723,32')
    # print('ok')
    #
    # reponse2= objService.getWfsFilterLayerWithPropertyEgale(layerName='ca_feux_close_scale',
    #                 propertyName='exercice', valeurEgaleA='2012')


    # list_polygon = objService.getWfsFilterLayerWithPropertyEgale(layerName='ms:ca_feux_close_scale',
    #                                                              propertyName='exercice', valeurEgaleA='2012')
    # print('ici')

    # objService = RequeteServiceWeb(repSavOutput='C:/Logiciels/temp/josee')
    list_polygon = objService.getWfsFilterLayerWithPropertyEgale(layerName='ms:feuillets_20k',
                                                                 propertyName='feuillet', valeurEgaleA='21L12NO')
    print('ok')


    # params = {
    #         'SERVICE': 'WFS',
    #         'VERSION': '2.0.0',
    #         'REQUEST': 'GetFeature',
    #         'TYPENAMES': 'ori_pee_close_scale',
    #         'OUTPUTFORMAT': 'GEOJSON',
    #         'FILTER':  '(<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo matchCase="true"><PropertyName>geocode</PropertyName><Literal>-26282,28+540723,32</Literal></PropertyIsEqualTo></Filter>)'

    #         }
    # url='https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?'
    # reponse = requests.get(url, params)

    url = 'https://pregeoegl.msp.gouv.qc.ca/ws/mffpecofor.fcgi?'

    params = {
        'SERVICE': 'WMS',
        'VERSION': '1.3.0',
        'REQUEST': 'GetFeatureInfo',
        # 'FORMAT': 'image/png',
        'QUERY_LAYERS': 'nord_photo_oblique',
        'LAYERS': 'nord_photo_oblique',
        # 'DPI': '96',
        # 'MAP_RESOLUTION': '96',
        # 'FORMAT_OPTIONS': 'dpi:96',
        'FILTER': '(<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo matchCase="true"><PropertyName>NOM_PHOTO</PropertyName><Literal>_DDD2941.jpg</Literal></PropertyIsEqualTo></Filter>)',
        # 'FILTER': '(%3CFilter%20xmlns%3D%22http%3A%2F%2Fwww.opengis.net%2Fogc%22%3E%3CPropertyIsEqualTo%20matchCase%3D%22true%22%3E%3CPropertyName%3EtypeAppareil%3C%2FPropertyName%3E%3CLiteral%3ERadar%20photo%20fixe%3C%2FLiteral%3E%3C%2FPropertyIsEqualTo%3E%3C%2FFilter%3E)',
        # 'INFO_FORMAT': 'text/plain',
        # 'INFO_FORMAT': 'application/json', ## non pas dispo pour GetFeatureInfo
        # 'INFO_FORMAT': 'application/vnd.ogc.gml',
        'FEATURE_COUNT': '5',
        'I': '50',
        'J': '50',
        'CRS': 'EPSG:3857',
        # 'STYLES': '',
        'WIDTH': '101',
        'HEIGHT': '101',
        'BBOX': '-7997104.281409148,5677667.427515962,-7750059.805991458,5924711.9029336525'
    }
    reponse = requests.get(url, params)
    print('ici')
