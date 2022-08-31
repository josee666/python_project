
from serviceOGR import ServiceOGR
from decorateur import decorateur_TimeFonction
import os

def getListShp(pathDossier):
    listFil = os.listdir(pathDossier)
    listShp = []

    for fil in listFil:
        if fil == 'total.shp':
            continue
        if fil[-3:] == 'shp':
            listShp.append("{0}/{1}".format(pathDossier, fil))

    return listShp


@decorateur_TimeFonction
def mergeShp(listShp):

    # pathGdal = "G:/OutilsProdDIF/modules_communs/gdal/gdal3.1.3"
    # pathGdal = "C:/MrnMicro/Applic/gdal/2.3.2"
    pathGdal = "C:/MrnMicro/Applic/gdal/2.3.2"
    objServiceOgr = ServiceOGR(pathGdal)
    pathNomShpTotal = "{}/total.shp".format(pathDossier)
    for leShp in listShp:
        cmdAppend = 'ogr2ogr -f "Esri shapefile" "{0}" "{1}" -append'.format(pathNomShpTotal, leShp)
        try:
            objServiceOgr.lancement_cmd(cmdAppend)
        except:
            print('oups probleme avec shp: {}'.format(leShp))



if __name__ == '__main__':

    # pathDossier = "G:/Fdif/Transit/GauDaf/resultat"
    pathDossier = "E:/Python/Projet_3_4/mergeShp/resultat"
    # pathDossier = "C:/Logiciels/temp/resultat"

    listShp = getListShp(pathDossier)
    mergeShp(listShp)

    print('ici')


