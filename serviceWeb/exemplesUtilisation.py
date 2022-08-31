
from classRequeteServiceWeb import *

#NB: Dans tous les exemples un fichier .geojson contenant le resultat de la requete est sauvegardé dans le repSavOutput

objService = RequeteServiceWeb(repSavOutput='C:/Logiciels/temp/josee', projection ="EPSG:32198")


# Ex1 - avoir le polygon + info du peup xyz
reponse = objService.getWFSPeuplementFromGeocode('-261463,86+312002,47')

# Ex2 - sort tous les feux ou exercice = 2012
# reponse= objService.getWfsFilterLayerWithPropertyEgale(layerName='ca_feux_close_scale',
#                 propertyName='exercice', valeurEgaleA='2012')

# Ex3 - avoir la geom + info du feuillet 21L12NO
# list_polygon = objService.getWfsFilterLayerWithPropertyEgale(layerName='ms:feuillets_20k',
#                                                              propertyName='feuillet', valeurEgaleA='21L12NO')

# Ex4 - la placette avec id = 1701203701
# reponse = objService.getWfsFilterLayerWithPropertyEgale(layerName='sond_pet5',
#                 propertyName='id_pe', valeurEgaleA='1701203701')

# Ex5 - le point + info de la caserne de pompier de la ville de Donnacona
# objService = RequeteServiceWeb(url='https://geoegl.msp.gouv.qc.ca/ws/igo_gouvouvert.fcgi?', repSavOutput='C:/Logiciels/temp/josee')
# listPoint = objService.getWfsFilterLayerWithPropertyEgale(layerName='CASERNE',
#                 propertyName='ville', valeurEgaleA='Donnacona')