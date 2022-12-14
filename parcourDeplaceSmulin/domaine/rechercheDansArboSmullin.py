import os
import xlsxwriter
from datetime import datetime
import shutil


from tkinter import messagebox

class RechercheDansArboSmullin:

    def __init__(self, dosFichierSortie):

        self.dosSmullinProjProv = r"""E:\a_temp\lidarTest\ex_smullin\proj_prov"""
        # self.dosSmullinProjProv = r"""\\Smullin\lidar\FORET\PRODUITS_DERIVES\Projet_Provincial"""
        # self.dosSmullinProjProv = r"""\\Smullin\lidar\public"""  V1

        self.dosFichierSortie = dosFichierSortie
        # self.dosSmullinPublic = r"""\\Smullin\lidar\public"""
        # self.dosSmullinPublic = r"""\\Smullin\lidar\FORET\PRODUITS_DERIVES\Projet_Provincial"""   V1
        self.dosSmullinPublic = r"""E:\a_temp\lidarTest\ex_smullin\public"""

        self.workbook = None
        self.worksheet = None

        self.noLigneXlsRendu = 0

        self.creerFichierXlSortie()

    def date_actuelle(self):
        """ Fonction qui retourne l'annee du systeme
        Exemple: 2017_12_01 """
        date_time = datetime.now()
        date_format = date_time.strftime("%Y_%m_%d %Hh%Mmin%Ssec")

        return date_format[:10]

    def date_formate(self):
        """ Fonction qui retourne date et heure:
         Exemple: 2016_10_28 11h50min22sec
        """
        date_time = datetime.now()
        date_format = date_time.strftime("%Y_%m_%d_%Hh%Mmin%Ssec")
        return date_format


    def creerFichierXlSortie(self):

        nomFil = "{}/SmullinRecherche_{}.xlsx".format(self.dosFichierSortie, self.date_formate())

        self.workbook = xlsxwriter.Workbook(nomFil)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_column('A:A', 30)
        self.worksheet.set_column('B:B', 120)
        self.worksheet.set_column('B:B', 120)
        self.worksheet.write('A1', 'Nom_fichier')
        self.worksheet.write('B1', 'Emplacement fichier')
        self.worksheet.write('C1', 'Action')


    def parcourArbo(self, deplace):
        xls_cpt_ligne = 2

        # listADeplace = ["MHC_FOCAL", "PENTES_5M"] V1
        listADeplace = ["MHC", "PENTES", "MNT"]   # V2

        # listBizzare = [".ZIP", "LOG", ".KML", "INFO", ".RHISTORY"]
        dosRecherche = r"""\\Smullin\lidar\PUBLIC\PRODUITS_DERIVES\Projet_Provincial"""

        listFil = os.listdir(dosRecherche)

        for unFil in listFil:

            if unFil != "Thumbs.db":
                idx_tiret = unFil.index("_")
                idxPoint = unFil.index(".")

                if "Ombre" in unFil:
                    idx_tiret = unFil.rfind("_")

                feuillet = unFil[idx_tiret+1:idxPoint]
                feuillet250k = feuillet[:3]

                pathFil = dosRecherche + "/{}".format(unFil)
                dosDest = r"""\\Smullin\lidar\PUBLIC\{0}\{1}""".format(feuillet250k, feuillet)

                dest = r"""\\Smullin\lidar\PUBLIC\{0}\{1}\{2}""".format(feuillet250k, feuillet, unFil)

                try:
                    # print("deplace: {0}\nici: {1}".format(pathFil, dest))
                    if not os.path.exists(dosDest):
                        os.makedirs(dosDest)

                    shutil.move(pathFil, dest)


                except:
                    print("impossible de d??placer")
                    messagebox.showwarning("Probl??me", "Probl??me avec le d??placement de ce fichier: {} - Veuillez vous assurez que le fichier n'est pas ouvert.".format(pathFil))



        #
        #
        # for root, dirs, files in os.walk(self.dosSmullinProjProv):
        #     # print(root)
        #     # print(dirs)
        #     # print(files)
        #
        #     # trouver les a deplace
        #     for unFichier in files:
        #         if "FOCAL" not in unFichier.upper() and "5M" not in unFichier.upper():  # V2
        #             for elem in listADeplace:
        #                 if elem in unFichier.upper():
        #
        #                     # ecrire workbook
        #                     self.worksheet.write('A{}'.format(xls_cpt_ligne), u'{}'.format(unFichier))
        #                     self.worksheet.write('B{}'.format(xls_cpt_ligne), u'{}'.format(root))
        #                     if not deplace:
        #                         self.worksheet.write('C{}'.format(xls_cpt_ligne), "D??plac??")
        #                         xls_cpt_ligne = xls_cpt_ligne + 1
        #
        #                     if deplace:
        #                         pathFil = root + "/" +unFichier
        #                         pathNorm = os.path.normpath(root)
        #                         pathSplit = pathNorm.split("\\")
        #                         dest = self.dosSmullinPublic + "/" + pathSplit[-2] + "/" + pathSplit[-1]
        #                         #todo a verif si ici c'est ok
        #
        #                         try:
        #                             if not os.path.exists(dest):
        #                                 os.makedirs(dest)
        #
        #                             shutil.move(pathFil, dest+ "/" +unFichier)
        #                             self.worksheet.write('C{}'.format(xls_cpt_ligne), "D??plac??")
        #                             xls_cpt_ligne = xls_cpt_ligne + 1
        #
        #                         except:
        #                             print("impossible de d??placer")
        #                             messagebox.showwarning("Probl??me", "Probl??me avec le d??placement de ce fichier: {} - Veuillez vous assurez que le fichier n'est pas ouvert.".format(pathFil))
        #                             self.worksheet.write('C{}'.format(xls_cpt_ligne), "NON D??PLAC??-probleme rencontr??... Veuillez vous assurez que le fichier n'est pas ouvert.")
        #
        #                             xls_cpt_ligne = xls_cpt_ligne + 1
        #
        #         # Les fcihiers bizarres
        #         if unFichier[-3:].upper() in ["ZIP", "LOG", "KML", "NFO", "ORY", ".DB"]:
        #
        #             self.worksheet.write('A{}'.format(xls_cpt_ligne), u'{}'.format(unFichier))
        #             self.worksheet.write_url('B{}'.format(xls_cpt_ligne), u'{}'.format(os.path.join(os.path.normpath(root))))
        #             self.worksheet.write('C{}'.format(xls_cpt_ligne), "A verfifier: fichier non connu")
        #
        #             xls_cpt_ligne = xls_cpt_ligne + 1