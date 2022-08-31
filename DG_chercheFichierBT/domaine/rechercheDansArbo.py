
import os
import xlsxwriter
from datetime import datetime


class RechercheDansArbo:

    def __init__(self, dosDepart, listDossierARecherche, dosFichierSortie):

        self.dosDepart = dosDepart
        # self.listDossierARecherche = listDossierARecherche
        self.setDossierARecherche = set(listDossierARecherche)
        self.dosFichierSortie = dosFichierSortie

        self.workbook = None
        self.worksheet = None
        self.setFichierTrouve = ()

        self.fichierTrouve = []
        self.noLigneXlsRendu = 0

        self.creerFichierXlSortie()

    def date_actuelle(self):
        """ Fonction qui retourne l'annee du systeme
        Exemple: 2017_12_01 """
        date_time = datetime.now()
        date_format = date_time.strftime("%Y_%m_%d %Hh%Mmin%Ssec")

        return date_format[:10]


    def creerFichierXlSortie(self):

        nomFil = "{}/recherche_{}.xlsx".format(self.dosFichierSortie, self.date_actuelle())
        # if os.path.exists(nomFil):
        #     os.remove(nomFil)

        self.workbook = xlsxwriter.Workbook(nomFil)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_column('A:A', 20)
        self.worksheet.set_column('B:B', 100)
        self.worksheet.write('A1', 'Nom_fichier')
        self.worksheet.write('B1', 'Emplacement fichier')


    def parcourArbo(self):
        xls_cpt_ligne = 2

        for root, dirs, files in os.walk(self.dosDepart):
            # print(root)
            # print(dirs)
            # print(files)
            setRepertoire = set(dirs)


            # pour recherche exact dans le fichier txt
            # result = set(self.setDossierARecherche.intersection(setRepertoire))

            for rep in setRepertoire:
                for aCherche in self.setDossierARecherche:
                     if aCherche == rep or aCherche+' ' in rep or aCherche+'_' in rep or aCherche+'-' in rep:
                     # if aCherche in rep:

                        print(aCherche)
                        self.fichierTrouve.append(aCherche)
                        # ecrire workbook
                        self.worksheet.write('A{}'.format(xls_cpt_ligne), u'{}'.format(rep))
                        self.worksheet.write_url('B{}'.format(xls_cpt_ligne), u'{}'.format(os.path.join(os.path.normpath(root), rep)))
                        xls_cpt_ligne = xls_cpt_ligne+1

            # print('ici')
        self.noLigneXlsRendu = xls_cpt_ligne


    def gestionListNonTrouve(self):

        setTrouver = set(self.fichierTrouve)
        nonTrouve = self.setDossierARecherche - setTrouver
        # self.noLigneXlsRendu +=2
        # self.worksheet.write('A{}'.format(self.noLigneXlsRendu), u'Dossiers non trouvés: ')
        self.noLigneXlsRendu += 1
        for i in nonTrouve:

            self.worksheet.write('A{}'.format(self.noLigneXlsRendu), u'{}'.format(i))
            self.worksheet.write('B{}'.format(self.noLigneXlsRendu), u'{}'.format("NON TROUVÉ"))
            self.noLigneXlsRendu += 1


