

from ClassConvertisseurGdb2sqlite import *
from tkinter import messagebox
import os
import shutil


class Prep250k:
    def __init__(self):

        self.leConvertiseurSqlite = ConvertisseurGdb2Sqlite("")
        self.dos_dep = ''

    def execute(self, dosDep):
        tempsDebut = time.time()
        self.dos_dep = dosDep

        listDos250k = os.listdir(self.dos_dep)


        for dos250k in listDos250k:
            #  21L
            path250k = self.dos_dep + "/" + dos250k
            liste2Dos = os.listdir(path250k)
            for dos in liste2Dos:
                if dos[-3:] == 'zip':
                    liste2Dos.remove(dos)

            for dos in liste2Dos:
                # 21L_GDB
                if dos[-3:] in ["GDB", "gdb"]:


                    listeGdb = os.listdir(path250k +"/" + dos)
                    for gdb in listeGdb:
                        # PENTE_250K_21L.gdb
                        if gdb[-4:] in [".gdb", ".GDB"]:
                            pathGdb = path250k +"/" + dos +"/" + gdb
                            dosBdSortie = path250k + "/" + dos[:-3] + "SQL"
                            if not os.path.exists(dosBdSortie):
                                os.mkdir(dosBdSortie)

                            bdSortie = dosBdSortie+"/" +gdb[:-4] +".sqlite"
                            if os.path.exists(bdSortie):
                                os.remove(bdSortie)

                            nomGdbSplit = gdb.split("_")
                            nomCouche = nomGdbSplit[0] +"_"+ nomGdbSplit[2][:-4]



                            # convertir

                            self.leConvertiseurSqlite.setSqlite(bdSortie)
                            self.leConvertiseurSqlite.setGdbAConvertir(pathGdb)

                            try:
                                self.leConvertiseurSqlite.OGR_creer_bdSqlite_avec_GDBuneSeuleCouche(nomCouche)
                            except:
                                self.leConvertiseurSqlite.OGR_creer_bdSqlite_avec_GDBcomplete()



            # zippage
            liste2Dos = os.listdir(path250k) # on recommence pour attrapé les dossier SQL creer
            for dos in liste2Dos:
                # 21L_GDB
                if dos[-3:] != "zip":
                    dosAZip = path250k + "/"+ dos
                    if os.path.exists(dosAZip+".zip"):
                        os.remove(dosAZip+".zip")
                    shutil.make_archive(dosAZip, 'zip', dosAZip)


        timeTot = time.time()
        temp_tot = round((timeTot - tempsDebut) / 60, 2)
        print("TRAITEMENT REUSSI")
        print(" JM - temps TOTALE= {}".format(temp_tot))
        messagebox.showinfo("Information", "Traitement terminé avec succès. Temps totale = {} minutes".format(temp_tot))