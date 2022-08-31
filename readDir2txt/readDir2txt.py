import os

from services.serviceTxt import *



if __name__ == '__main__':

    pathDirMHC = "E:/mapserver7/replicat/DIF_DATA/lidar/mnt"
    pathDirombre = "E:/mapserver7/replicat/DIF_DATA/lidar/OMBRE"
    filSortie = "E:/a_temp/replcatOMBRE.txt"
    #
    # objServiceTxt = ServiceTxt(filSortie)
    # contenuDir = os.listdir(pathDir)
    # for i in contenuDir:
    #     objServiceTxt.ecrire(i)

    contenuMHC = os.listdir(pathDirMHC)
    contenuOmbre = os.listdir(pathDirombre)
    listMHC = [] #MHC_21M10NE.tif
    listOmb = []  # MNT_Ombre_12E03NE.tif
    for i in contenuMHC:
        listMHC.append(i[-11:-4])

    for i in contenuOmbre:
        listOmb.append(i[-11:-4])

    dif = set(listOmb)- set(listMHC)
    for i in set(listOmb):
        if i not in set(listMHC):
            print('i')
    print('finit')