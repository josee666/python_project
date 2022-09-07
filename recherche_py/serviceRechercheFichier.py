


import os
import pathlib



class ServiceRechercheFichier():

    def __init__(self, dosDepart, listExtensionFichier, listExpressionATrouve ):
        self.extensions = listExtensionFichier
        self.dosDepart = os.path.normpath(dosDepart)
        self.listExpATrouve = listExpressionATrouve

        self.listFileARegarder = []
        self.dictFileTrouve = {} ## nomfile : [path, listNoLigneTrouve]
        self.dictTrouve = {} ## expression : [path, listNoLigneTrouve]
        self.listExpFileTrouve = []
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

        self.listFileARegarder = self.getListFile()
        self.openAllAndSearch()



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
                print("ce ficrier ne s'ouvre pas avec open... a faire plus tard")
                # listFileCantOpen.append(file)
                self.filesProblemeLecture.append((file, e))
            try:
                for line in openFile:
                    compteurLigne += 1

                    for exp in self.listExpATrouve:
                        if exp in line:
                            # print('Trouvé', exp, file)

                            keyNameFile = file.replace('\\', '_')

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
                print("check ici prob de lecture dans le fichier $%? encodage")
                self.filesProblemeLecture.append((file, e))
                continue

        self.printFileProbleme()
        print('fin')




    def exportResult(self):
        print('check; from tabulate import tabulate package')

    def printFileProbleme(self):
        print('les files incapables lire: ' )
        for i in self.filesProblemeLecture:
            print(i)

# for file in self.listFileARegarder:
#     compteurLigne = 0
#     keyFileInDict = file in self.dictFileTrouve
#     try:
#         openFile = open(file, encoding='utf8')
#     except Exception as e:
#         print("ce fihcier ne s'ouvre pas avec open... a faire plus tard")
#         listFileCantOpen.append(file)
#
#     for line in openFile:
#         compteurLigne += 1
#
#         for exp in self.listExpATrouve:
#             if exp in line:
#                 print('Trouvé', exp, file)
#                 # check si dict file exist et si dict exp existe
#                 if not keyFileInDict:
#                     self.dictFileTrouve[file]= {}
#                 # check si dict Exp exist
#                 if not exp in self.dictFileTrouve[file].values():
#                     print('existe pas')
#                     self.dictFileTrouve[file] = {exp : [compteurLigne]}
#                 else:
#                     print('ici')
#



if __name__ == '__main__':

    pathDep = "D:/Python\projetGit/donneeTest/recherche_py"
    servSearch = ServiceRechercheFichier(pathDep, ['.py', '.txt'], ['valid_essence_famille', 'self.repTravail' ])

    # pathDep = "D:\\"
    # pathDep = "D:\FOX_prog"
    # servSearch = ServiceRechercheFichier(pathDep, ['.py'], ['getNullouBlanc'])

    servSearch.search()
    print('ici')
