


import os
import pathlib

from tabulate import tabulate





class ServiceRechercheFichier():

    def __init__(self, dosDepart, listExtensionFichier, listExpressionATrouve ):
        self.extensions = listExtensionFichier
        self.dosDepart = os.path.normpath(dosDepart)
        self.listExpATrouve = listExpressionATrouve

        self.listFileARegarder = []
        self.dictFileTrouve = {} ## nomfile : [path, listNoLigneTrouve]
        # self.dictTrouve = {} ## expression : [path, listNoLigneTrouve]
        # self.listExpFileTrouve = []
        self.filesProblemeLecture = []

        # self.testdictfile = {
        #                 'filex':{
        #                         'exp1': [2,3,4],
        #                         'exp2': [5,6]
        #                         },
        #                 'filey': {
        #                         'exp1': [8,9,5],
        #                         'exp2': [50,60]
        #                         }
        #                 }


    def search(self):

        self.checkDosExist(self.dosDepart)
        self.listFileARegarder = self.getListFile()
        self.openAllAndSearch()
        self.exportResultHtml()

    def checkDosExist(self, pathDos):
        if not os.path.exists(pathDos):
            raise Exception("Le dossier {} n'existe pas, veuillez corriger!!".format(pathDos))

    def getListFile(self):

        listfile = []

        for root, dirs, files in os.walk(self.dosDepart):
            if 'RECYCLE.BIN' in root:
                continue
            # trouver les a deplace
            for unFichier in files:
                if pathlib.Path(unFichier).suffix in self.extensions:
                    # print('fichier a regarder')
                    pathFil = root + "\\" + unFichier
                    listfile.append(pathFil)
        return listfile


    def openAllAndSearch(self):
        # fileProblemeLecture = []
        # listFileCantOpen = []
        openFile = ''

        for file in self.listFileARegarder:
            compteurLigne = 0
            try:
                openFile = open(file, encoding='utf8')
            except Exception as e:
                print("ce fichier ne s'ouvre pas avec open... a faire plus tard")
                # listFileCantOpen.append(file)
                self.filesProblemeLecture.append((file, e))
            try:
                for line in openFile:
                    compteurLigne += 1

                    for exp in self.listExpATrouve:
                        if exp in line:
                            # print('Trouvé', exp, file)

                            # keyNameFile = file.replace('\\', '_')
                            keyNameFile = file.replace('\\', '/')

                            # check si dict file exist et si dict exp existe
                            if keyNameFile not in list(self.dictFileTrouve.keys()):
                                self.dictFileTrouve[keyNameFile]= {exp : [compteurLigne]}

                            else: ##le file exist dans la dict
                                # check si dict Exp exist
                                trouveExpression = False
                                leDictExp = self.dictFileTrouve[keyNameFile]
                                if exp in list(leDictExp.keys()):
                                    leDictExp[exp].append(compteurLigne)
                                    trouveExpression = True
                                    continue
                                if not trouveExpression:
                                    self.dictFileTrouve[keyNameFile][exp] = [compteurLigne]
            except Exception as e:
                print (e)
                # print("check ici prob de lecture dans le fichier $%? encodage")
                self.filesProblemeLecture.append((file, e))
                continue

        self.printFileProbleme()
        print('fin')




    def exportResultHtml(self):
        # print('check; from tabulate import tabulate package')
        style = """<style>
                h2{color:red}
                th, td {
                  border: 1px solid;
                }
                table {
                  width: 100%;
                   padding: 8px;
                }
                td {
                text-align: center
                background-color: #04AA6D
                color: white
                }
                tr:nth-child(even){background-color: #f2f2f2;}
                tr:nth-child(1) {
                font-weight: bolder;
                }
                tr:hover {background-color: #ddd;}
                
                </style>
            """

        titreCol = ['Fichier', 'Expression trouvée', 'no Ligne']
        # listImprim = ['fichieX', 'exp1', '1,2,3,4']
        # listImprim2 = ['fichieX', 'exp2', '5,6']
        # listImprim3 = ['fichieZ', 'exp1', '100, 1223']
        #
        # tab = [titreCol, listImprim, listImprim2, listImprim3 ]
        # print(tabulate(tab, tablefmt='html'))

        listTot = []
        listTot.append(titreCol)

        for fil, dictExp in self.dictFileTrouve.items():
            print(fil, dictExp)
            for exp, listNo in dictExp.items():
                listTot.append([fil, exp, listNo])

        tabHtml = tabulate(listTot, tablefmt='html')

        titreDoc = "Résultat recherche de fichier"

        html_file = open('exportResult.html', 'w')
        html_file.write(style)
        html_file.write("<h2>{}</h2>".format(titreDoc))
        html_file.write(tabHtml)
        # html_file.write(tes)
        html_file.close()


    def printFileProbleme(self):
        if len(self.filesProblemeLecture) > 0:
            print('les files incapables lire: ' )
            fileProb = open('fichiersProblemeLecture', 'w')
            for i in self.filesProblemeLecture:
                print(i)
                fileProb.write(i[0])
            fileProb.close()





if __name__ == '__main__':

    # pathDep = "G:\OutilsProdDIF\modules_communs\python27"
    # pathDep = "D:\python\gitProjet\donneeTests\ServRecherche"
    # pathDep = "D:/Python\projetGit/donneeTest/recherche_py"
    # servSearch = ServiceRechercheFichier(pathDep, ['.py'], [ 'getNullouBlanc' ])

    pathDep = "D:\\"
    # pathDep = "D:\FOX_prog"
    servSearch = ServiceRechercheFichier(pathDep, ['.py'], ['createTable('])

    servSearch.search()
    print('ici')
