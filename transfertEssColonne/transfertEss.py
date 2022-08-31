import sqlite3

from serviceBdSqlite import *
from serviceOGR import *


# def creerColonneEssence():
#     sql = "alter table"


class TransfertEssColonne():

    def __init__(self, pathFileIn, pathGdal=''):
        self.pathFileIn = pathFileIn
        self.pathGpkg = self.pathFileIn[0:-3]+'gpkg' ## shp ou gdb idem -3
        # self.pathGdal = "C:/Logiciels/gdal2_3_2"
        self.pathGdal = "G:\\OutilsProdDIF\\modules_communs\\gdal\\gdal3.1.3"
        self.servOgr = ServiceOGR(self.pathGdal)
        self.creerGpkg()
        self.nomTab = ''
        self.servBd = ServiceBdSqlite(self.pathGpkg, mode_spatialite=False)
        self.listEssSup = []
        self.listEssInf = []


    def effaceGpkg(self):
        if os.path.exists(self.pathGpkg):
            os.remove(self.pathGpkg)


    def creerGpkg(self):

        self.effaceGpkg()
        if self.pathFileIn[-3:] == 'shp':
            self.servOgr.shp2gpkg(self.pathFileIn, self.pathGpkg)
        else:
            self.servOgr.gdb2gpkg_touteLesTab(self.pathFileIn, self.pathGpkg)

    def transfertEssence(self):

        self.checkPlusUneTab()
        self.getListEssencePresente()
        self.creeColEss()
        self.remplirColEss()
        self.servOgr.addSpatialIndex(self.pathGpkg, self.nomTab, 'geom')
        self.exportGdb()
        # self.servBd.ferme_connexionBD()

        print('fin traitement')



    def checkPlusUneTab(self):
        listTab = self.servBd.getListTableBd()
        if len(listTab) > 1:
            raise Exception("il y a plus d'une table dans la bd, le systeme ne sais pas laquelle traiter...")

        self.nomTab = listTab[0]


    def getListEssencePresente(self):
        ## sortir les differentes essence presente SUP et INF

        listSup = []
        listInf = []

        for ess in range(1, 8):
            sql = """ select distinct ("et{0}_ess{1}") from "{2}" """.format(1, ess, self.nomTab)
            self.servBd.executeRequete(sql)
            result = self.servBd.leCursor.fetchall()
            listSup += self.servBd.list_tup2list(result, 0)
            # setEssSup.add(set(list))

        self.listEssSup = list(set(listSup)) ## Enleve doublons
        try:
            self.listEssSup.remove(None)
        except:
            pass

        for ess in range(1, 8):
            sql = """ select distinct("et{0}_ess{1}") from "{2}" """.format(2, ess, self.nomTab)
            self.servBd.executeRequete(sql)
            result = self.servBd.leCursor.fetchall()
            listInf += self.servBd.list_tup2list(result, 0)
            # setEssSup.add(set(list))

        self.listEssInf = list(set(listInf))

        try:
            self.listEssInf.remove(None)
        except:
            pass


        self.listEssSup.sort()
        self.listEssInf.sort()
        # listEss = getListEssencePresente()
        # creerColonneEssence()


    def creeColEss(self):
        ## sup etage 1
        for ess in self.listEssSup:
            self.servBd.ajoutColonne(self.nomTab, '{}_SUP'.format(ess), 'INTEGER')

        ## inf etage 2
        for ess in self.listEssInf:
            self.servBd.ajoutColonne(self.nomTab, '{}_INF'.format(ess), 'INTEGER')


    def remplirColEss(self):
        for ess in self.listEssSup:
            nomCol =  ess +'_SUP'
            for cpt in range(1, 8):
                # parcour les ess-prc de 1 a 7 jusqu'a trouve la bonne essence et met cela dedans nouv col BOP_SUP
                sql = """ update {0} set "{1}" = ET1_PC{2} where ET1_ESS{2} == '{3}'
                """.format(self.nomTab, nomCol, cpt, ess)
                self.servBd.executeRequete(sql, commit=True)

            # mettre prc vrai
            sql = """ update {0} set {1} = {1}*10 where {1} != 0 """.format(self.nomTab, nomCol)
            self.servBd.executeRequete(sql, commit=True)
            sql = """ update {0} set {1} = 100 where {1} = 0 """.format(self.nomTab, nomCol)
            self.servBd.executeRequete(sql, commit=True)
            # mettre les null = 0
            sql = """ update {0} set {1} = 0 where {1} is null """.format(self.nomTab, nomCol)
            self.servBd.executeRequete(sql, commit=True)

        for ess in self.listEssInf:
            nomCol =  ess +'_INF'
            for cpt in range(1, 8):
                sql = """ update {0} set "{1}" = ET2_PC{2} where ET2_ESS{2} == '{3}'
                """.format(self.nomTab,nomCol, cpt, ess)
                self.servBd.executeRequete(sql, commit=True)

            # mettre prc vrai
            sql = """ update {0} set {1} = {1} *10 where {1} != 0 """.format(self.nomTab, nomCol)
            self.servBd.executeRequete(sql, commit=True)
            sql = """ update {0} set {1} = 100 where {1} = 0 """.format(self.nomTab, nomCol)
            self.servBd.executeRequete(sql, commit=True)

            ## change null pour 0
            sql = """ update {0} set {1} = 0 where {1} is null """.format(self.nomTab, nomCol)
            self.servBd.executeRequete(sql, commit=True)


    def exportGdb(self):
        pathGdb = "{}_transfEss.gdb".format(self.pathGpkg[:-5])
        self.servOgr.ecraseSiExiste(pathGdb)
        self.servOgr.creerGDB_aPartirGpkg(pathGpkg=self.pathGpkg, newNomGdb=pathGdb)

if __name__ == '__main__':
    # pathshp = "C:/job/python/transfert_ess/donnee/c21112_22D06SE_L1.shp"
    pathshp = "D:\\Python\\projetGit\\donneeTest\\transfertEss\\in\\inFile.shp"
    objTransfert = TransfertEssColonne(pathshp)
    objTransfert.transfertEssence()

