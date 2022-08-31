from serviceBdSqlite import *
from serviceOGR import *
import shutil


class ErreurServiceSimplification(Exception):
    """ JM 2018-08
        Classe exception lancée lors d'un probleme avec le serviceBD.

        Exemple apel:   try:
                            ...
                            raise ErreurServiceBD("probleme xyz")
                        except ErreurServiceBD as e:
                            print (e.message)
    """
    def __init__(self, message="Une erreur est survenu avec le serviceSimplification", typeErreur='ErreurServiceSimplification'):
        self.message = message
        self.typeErreur = typeErreur

    def __str__(self):
        return repr(self.message)


class ServiceSimplification:

    ### Exemple :

    ###

    def __init__(self, path_Bd):

        self.path_bd = path_Bd

        self.gpkg = False
        if self.path_bd[-4:] == 'gpkg':
            self.gpkg = True
        elif self.path_bd[-6:] != 'sqlite':
            raise ErreurServiceSimplification('la base de donnée indiqué doit etre un GPKG ou une SQLITE pour fonctionner. Vous avez indiquez {}'.format(self.path_bd))

        self.serviceBd = ServiceBdSqlite(self.path_bd, mode_spatialite=True)
        self.serviceOgr = ServiceOGR(pathGdal="G:/OutilsProdDIF/modules_communs/gdal/gdal3.1.3")


    def creerCoucheSimplifie(self, nomCoucheASimplifier, niveauSimplification):
        # Le niveau de simplifiocation est une valeur numerique qui varie de 0.1 a 15
        # ** Pourrait etre > 15 mais normalement plus de 15 creera des formes tres carré

        self.serviceBd.ST_simplifie_createNewTab(nomCoucheASimplifier, niveauSimplification)


    def creerTab_nbSommets_differentNivSimplification(self, nomCoucheASimplifier, nomColonneId):
        ### indiquer la colonne ID presente dans la table qui permetra de différencier les polygones
        # Exemple:  objectid, fid, geocode, etc

        self.serviceBd.ST_createTabNbSommetSimplification(nomCoucheASimplifier, nomColonneId)


    def creer6CouchesSimplifieesDifferentNiv(self, nomCoucheASimplifier):
        print('en traitement... veuillez patientez')
        self.serviceBd.ST_simplifie_createNewTab(nomCoucheASimplifier, 0.1)
        self.serviceBd.ST_simplifie_createNewTab(nomCoucheASimplifier, 0.5)
        self.serviceBd.ST_simplifie_createNewTab(nomCoucheASimplifier, 1)
        self.serviceBd.ST_simplifie_createNewTab(nomCoucheASimplifier, 5)
        self.serviceBd.ST_simplifie_createNewTab(nomCoucheASimplifier, 7)
        self.serviceBd.ST_simplifie_createNewTab(nomCoucheASimplifier, 10)
        print('Creation des 6 couches simplifiées terminé !!!!!')


    def export_couche(self, nomCoucheAExport, formatSortie):

        bdFolderPath = os.path.dirname(self.path_bd)


        pathNomFile = '{0}/{1}.{2}'.format(bdFolderPath, nomCoucheAExport, formatSortie)
        if os.path.exists(pathNomFile):
            shutil.rmtree(pathNomFile)

        if formatSortie == 'geojson':
            self.serviceOgr.creerGeojson_aPartirCoucheBd(pathNomGeojson=pathNomFile, pathBd=self.path_bd, nomCoucheBd= nomCoucheAExport)

        elif formatSortie == 'shp':
            self.serviceOgr.creerShapefile_aPartirCoucheBd(pathNomShp=pathNomFile, pathBd=self.path_bd, nomCoucheBd= nomCoucheAExport)
        else:
            raise ErreurServiceSimplification('Ce format pour export est inconnue= {}. Format possible : geojson ou shp'.format(formatSortie))


    def export_bd_complete_GDB(self):

        nomGdb = "{}.gdb".format(pathGpkg[:-5])
        if os.path.exists(nomGdb):
            shutil.rmtree(nomGdb)
        self.serviceOgr.creerGDB_aPartirGpkg(self.path_bd)



if __name__ == '__main__':

    # pathGpkg = "D:/Python/Projet_3_4/git/ServiceSimplification/donneeTest/newTest/ori.gpkg"
    pathGpkg = "D:\\Python\\projetGit\\donneeTest\\serviceSimplification\\newTest\\ori.gpkg"
    objServiceSimplification = ServiceSimplification(pathGpkg)

    # objServiceSimplification.creerTab_nbSommets_differentNivSimplification(nomCoucheASimplifier='Modifications_UG_2023', nomColonneId='OBJECTID')
    #
    objServiceSimplification.creer6CouchesSimplifieesDifferentNiv(nomCoucheASimplifier='Modifications_UG_2023')

    objServiceSimplification.export_bd_complete_GDB()
    objServiceSimplification.export_couche('Modifications_UG_2023_simp7', 'geojson')
    objServiceSimplification.export_couche('Modifications_UG_2023_simp7', 'shp')

    print('fin!!!!!!!!!')