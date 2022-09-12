# -*- coding: utf-8 -*-

from tkinter import Tk, Label, Button, Entry, E, W, END
from tkinter import filedialog as tkFileDialog
from tkinter import messagebox as tkMessageBox

from functools import partial
import threading

from transfertEss import *



class App_transfertEssence(Tk):
    # 2022-07
    # auteur - J
    # programme qui transfert le fichier plate ess-prc en ess-col.
    # ex: ET1_ESS1  - ET1_PC1                      SAB_SUP
    #       SAB     -   0       va devenir          100

    def __init__(self):

        Tk.__init__(self)

        self.geometry("700x220+600+250")
        self.title("Transfert essences ET_ESS_PRC en colonne ESS_SUP et ESS_INF")
        self.version = 1.1


        # Widget

        self.labelMessage = Label(self, text="Choisir un SHP ou une GDB de départ", fg="blue", font=("Helvetica", 11))
        self.labelMessage.grid(row=0,column=1, padx=70, pady=10, sticky=W)


        self.bt_gdb = Button(self, text="Indiquer la GDB départ", command=partial(self.jopen, "", "box_gdb" )) #command=self.jopen_dossier)
        self.bt_gdb.grid(row=2, column=0, padx=10, pady=10, sticky=W+E)

        self.box_gdb = Entry(self, width=80)
        self.box_gdb.grid(row=2, column=1, padx=10, pady=10)

        self.bt_shp = Button(self, text="Indique le SHP de depart", command=partial(self.jopen, "fil", "box_shp" )) #command=self.jopen_rep)
        self.bt_shp.grid(row=4, column=0, padx=10, pady=10)

        self.box_shp = Entry(self, width=80)
        self.box_shp.grid(row=4, column=1, padx=10, pady=10)

        self.bt_exe = Button(self, text="Exécuter", command=self.executer, fg="red", font="Verdana 10 bold")
        self.bt_exe.grid(row=6, column=1, sticky=W, padx=120, pady=20)

        self.bt_fer = Button(self, text="Fermer", command=self.destroy, width=5, height=1)
        self.bt_fer.grid(row=6, column=1, sticky=W, padx=220, pady=20)


        # attribut
        self.dos_dep = ''


    def jopen(self, option, nomBox):

        if option == "fil":
            repNom = tkFileDialog.askopenfilename(title="Pointer le fichier ", filetypes=[('ShapeFile', '*.shp')])
        else:
            repNom = tkFileDialog.askdirectory(title="Indiquer le repertoire")

        leBox = getattr(self, nomBox)

        leBox.delete(0, END)
        leBox.insert(0, repNom)


    def changeButtonState(self, state):
        # state choice disabled or normal
        self.bt_gdb['state']=state
        self.bt_shp['state']=state
        self.box_gdb['state']=state
        self.box_shp['state']=state
        self.bt_exe['state']=state




    def executer(self):
        def real_traitement():
            self.labelMessage['text'] = 'Traitement en cours, veuillez patientez'
            self.changeButtonState('disabled')
            try:
                if self.box_gdb.get():
                    self.dos_dep = self.box_gdb.get()
                elif self.box_shp.get():
                    self.dos_dep = self.box_shp.get()
                else:
                    raise Exception('Veuillez indiquer un fichier de départ!')

                objTransfert = TransfertEssColonne(pathFileIn=self.dos_dep, pathGdal="G:/OutilsProdDIF/modules_communs/gdal/gdal3.1.3")
                objTransfert.transfertEssence()

            except Exception as e:
                tkMessageBox.showerror('Un probleme est survenu', 'Erreur = {}'.format(e))
                self.changeButtonState('normal')
                raise


            tkMessageBox.showinfo('Traitement terminé', 'Une gdb et un gpkg avec les colonnes ESS_SUP et ESS_INF sont disponible au même emplacement')
            self.labelMessage['text'] = 'Traitement terminé!'
            self.changeButtonState('normal')


        threading.Thread(target=real_traitement).start()



if __name__ == '__main__':

    f = App_transfertEssence()
    f.mainloop()