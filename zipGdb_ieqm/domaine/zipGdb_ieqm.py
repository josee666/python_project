

from tkinter import messagebox
import os, sys
import shutil
import csv
from stat import ST_SIZE

# sys.path.append(r"\\Sef1271a\F1271g\OutilsProdDIF\modules_communs\python27\GestionDossierFichier\bin")
# from GestionDossierFichier import deployer_fichier_pth
# deployer_fichier_pth("modules_communs", "G:/OutilsProdDIF/modules_communs/python27", ['bin'])

from ClassConvertisseurGdb2sqlite import *


class ZipGdb_ieqm():
    def __init__(self, dosDepart, DosSortie, ecrase, leType):

        self.leConvertiseurSqlite = ConvertisseurGdb2Sqlite("")

        self.dos_depart = dosDepart
        self.dos_sortie = DosSortie
        self.ecrase = ecrase
        self.ori = False
        self.maj = False
        self.dendroLid = False

        self.setType(leType)


    def setType(self, leType):
        if leType == 'ori':
            self.ori = True
        elif leType == 'maj':
            self.maj = True
        elif leType == 'dendroLid':
            self.dendroLid = True


    def execute(self):

        tempsDebut = time.time()

        if self.dendroLid:
            nbZipFait = self.zipEtConverDendroLidSortirPoid(self.dos_depart)

        else:
            nbZipFait = self.parcourirArbo()

        timeTot = time.time()
        temp_tot = round((timeTot - tempsDebut) / 60, 2)
        print("TRAITEMENT REUSSI")
        print(" JM - temps TOTALE= {}".format(temp_tot))
        messagebox.showinfo("Information", "Traitement terminé avec succès!\nTemps totale = {} minutes. {} Zip fait lors du traitement!".format(temp_tot, nbZipFait))


    def creation_arborescence(self, path_a_cree):
        """ JM 2016-03-16
        Fonction qui créer si n'éxiste pas l'arborescence souhaite

        Exemple apell : creation_arborescence("E:/a_temp/dendroLidarCopy/21M")

                Si n'existe pas créera: a_temp, si n'existe pas creera dendroLidar, si n'existe pas creera 21M
        """

        if not os.path.exists(path_a_cree):
            os.makedirs(path_a_cree)


    def parcourirArbo(self):

        listDosNiv1 = os.listdir(self.dos_depart)
        nbZipFait = 0
        for dosNiv1 in listDosNiv1:

            pathUnDosNiv1 = self.dos_depart + "/" + dosNiv1

            if self.maj or self.ori:
                if dosNiv1[-4:] in [".gdb", ".GDB"]:
                    #  maj+ori : PRODUITS_IEQM_31I_10.gdb,

                    nomSplit = dosNiv1.split("_")
                    nomDossier = nomSplit[-2]
                    verGdb = nomSplit[-1]

                    dosACreer = self.dos_sortie + "/" + nomDossier
                    self.creation_arborescence(dosACreer)

                    nomGdb = dosNiv1
                    if self.maj:
                        nomGdb = "CARTE_ECO_MAJ_" +nomDossier + "_"+  verGdb

                    dosSortie = self.dos_sortie + "/"+ nomDossier +"/" + nomGdb[:-4] #.../sortiOutil/31I/PRODUITS_IEQM_31I_10'
                    gdbSortie = dosSortie + "/" +nomGdb                             # .../sortiOutil/31I/PRODUITS_IEQM_31I_10/PRODUITS_IEQM_31I_10.gdb'
                    filSortie = dosSortie + ".zip"                                  # /sortiOutil/31I/PRODUITS_IEQM_31I_10.zip'

                    filExiste = self.getFilExiste(filSortie)

                    if filExiste and not self.ecrase:
                        print("le fichier {} est présent et on ecrase pas, on passe".format(filSortie))
                        continue

                    elif filExiste and self.ecrase:
                        self.efface(filSortie)

                    self.faireZip(pathUnDosNiv1, dosSortie, gdbSortie)
                    nbZipFait += 1
            #
            # elif self.dendroLid and dosNiv1[-4:] not in [".gdb", ".GDB"] and not os.path.isfile(dosNiv1):
            #
            #     # 21M
            #
            #     lisDosNiv2 = os.listdir(pathUnDosNiv1)
            #     for dosNiv2 in lisDosNiv2:


        return nbZipFait




    def faireZip(self, filIn, dosOut, filOut):

#       # on veux que dedans le .zip ce soit XXXX.gdb et non direct le contenu de la GDB

        # copîe la gdb dans un dossier
        self.creation_arborescence(dosOut)
        shutil.copytree(filIn, filOut)

        # zippe le dossier
        shutil.make_archive(dosOut, 'zip', dosOut)
        # shutil.make_archive(filOut, 'zip', filIn)

        #ecraser dos Depart
        self.efface(dosOut, False)



    def getFilExiste(self, pathFil):

        filExiste = False
        if os.path.exists(pathFil):
            filExiste = True
        else:
            filExiste = False

        return filExiste

    def efface(self, pathAEcrase, fil=True):

        if fil:
            os.remove(pathAEcrase)
        else:
            shutil.rmtree(pathAEcrase)

  ####################################


    def zipEtConverDendroLidSortirPoid(self, dos_depart):
        """ Fonction qui parcour et zip les fichier dendro et donne fichier csv avec la taille
        *** attention les dossiers ne doivent pas existe... pas gerer
        """
        nbZipFait = 0
        with open(dos_depart + '/tailleZipLidar.csv', 'w') as csvfile:
            leCsv = csv.writer(csvfile, delimiter=';',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)

            list_dos_niv1 = os.listdir(dos_depart)

            # objConvertisseur = ConvertisseurGdb2Sqlite(None)

            nb = 1
            for dos1 in list_dos_niv1:
                # Niveau1 22D
                if len(dos1) > 3 or dos1[-4:] in [".gdb", ".GDB"]:
                    continue

                pathDos1 = dos_depart + "/" + dos1
                if os.path.isdir(pathDos1):
                    list_gdb = os.listdir(pathDos1)
                    for gdb in list_gdb:
                        ##CARTE_DENDRO_LIDAR_22D02NO.gdb
                        if len(gdb) < 26 or gdb[-4:] not in [".gdb", ".GDB"]:
                            continue

                        pathGdb = pathDos1 + "/" + gdb
                        if gdb != "Thumbs.db":
                            # creation des dossier
                            pathSplit = pathGdb.split("/")
                            nomGdb = pathSplit[-1]
                            gdbSplit = nomGdb.split('_')
                            dosFeuillet = gdbSplit[-1][:-4]

                            dosSqlAcreer = pathDos1 + "/" + dosFeuillet + "/" + nomGdb[:-4] + "_SQL"
                            dosGdbAcreer = pathDos1 + "/" + dosFeuillet + "/" + nomGdb[:-4] + "_GDB"

                            self.creation_arborescence(dosSqlAcreer)
                            self.creation_arborescence(dosGdbAcreer)

                            # creation Sqlite conversion
                            filSqlite = dosSqlAcreer + "/" + nomGdb[:-4] + ".sqlite"


                            if self.getFilExiste(filSqlite) and not self.ecrase:
                                print("le fichier {} est présent et on ecrase pas, on passe".format(filSqlite))
                                continue

                            elif self.getFilExiste(filSqlite) and self.ecrase:
                                self.efface(filSqlite)

                            self.leConvertiseurSqlite.setSqlite(filSqlite)
                            self.leConvertiseurSqlite.setGdbAConvertir(pathGdb)
                            self.leConvertiseurSqlite.OGR_creer_bdSqlite_avec_GDBcomplete()

                            # copier GDB dans dossier
                            dosGdb = dosGdbAcreer + "/" + gdb
                            if self.getFilExiste(dosGdb) and not self.ecrase:
                                print("le fichier {} est présent et on ecrase pas, on passe".format(dosGdb))
                                continue
                            elif self.getFilExiste(dosGdb) and self.ecrase:
                                self.efface(dosGdb, False)

                            shutil.copytree(pathGdb, dosGdb)

                            if self.getFilExiste(dosSqlAcreer+".zip"):
                                self.efface(dosSqlAcreer+".zip")
                            if self.getFilExiste(dosGdbAcreer + ".zip"):
                                self.efface(dosGdbAcreer + ".zip")

                            shutil.make_archive(dosSqlAcreer, 'zip', dosSqlAcreer)
                            shutil.make_archive(dosGdbAcreer, 'zip', dosGdbAcreer)

                            # apres zip on supp l'autre
                            shutil.rmtree(dosSqlAcreer)
                            shutil.rmtree(dosGdbAcreer)

                            # taille du zip
                            st = os.stat(dosGdbAcreer + ".zip")
                            taille = st[ST_SIZE]
                            taille_lisible = self.getHumanReadable(taille)

                            feuil = dosFeuillet
                            leCsv.writerow([feuil, taille_lisible])

                            nbZipFait += 2
        return nbZipFait


    def getHumanReadable(self, size, precision=2):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
            suffixIndex += 1  # increment the index of the suffix
            size = size / 1024.0  # apply the division
        return "%.*f%s" % (precision, size, suffixes[suffixIndex])




    # def effaceSiExiste(self, filAEcrase):
    #
    #     probleme = False
    #     if os.path.exists(filAEcrase):
    #         filExiste = True
    #         if self.ecrase:
    #             os.remove(filAEcrase)
    #         else:
    #             probleme
    #             pass
    #     return filExiste

    #
    #
    # def gdb2Sqlite(self, pathFilApresRepPointe, pathGdbAConvertir):
    #
    #     dest = self.dos_sortie + "/" + pathFilApresRepPointe[:-4] + "_SQL.sqlite"
    #     listDos = pathFilApresRepPointe.split('/')
    #
    #     # creer les dossiers dans rep sortie
    #     pathDosAcreer = ''
    #     for i in listDos:
    #         if listDos.index(i) != len(listDos-1):
    #             pathDosAcreer += i
    #
    #     self.creation_arborescence(pathDosAcreer)
    #
    #
    #     #conver
    #     self.leConvertiseurSqlite.setSqlite(dest)
    #     self.leConvertiseurSqlite.setGdbAConvertir(pathGdbAConvertir)
    #
    #     self.leConvertiseurSqlite.OGR_creer_bdSqlite_avec_GDBcomplete()








































