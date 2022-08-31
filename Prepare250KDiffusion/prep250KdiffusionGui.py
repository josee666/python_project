

# -*- coding: utf-8 -*-
import os
import shutil

from tkinter import Tk, Button, Label, Entry, E, W,END, filedialog, messagebox

# from tkFileDialog import askopenfilename, askdirectory


from tkinter import messagebox
from functools import partial
from prep250k import *


class App_prep250K(Tk):
    # Application developper pour ...
    # auteur - date

    def __init__(self):

        Tk.__init__(self)

        self.version = 2
        self.geometry("700x180+600+250")
        self.title("Preparation des gdb250K -> sqlite pour diffusion. Version: {}".format(self.version))
        self.prep250k = Prep250k()


        # Widget

        label = Label(self, text="Veuillez sélectionner le dossier parent. L'outil descend 2 niveaux. Par exemple choisir: Pente_250K. "
                                 "\nLe traitement prend environ 30 secondes par fichier.")
        label.grid(row=1,column=0, columnspan=2, padx=10, pady=10, sticky=W+E)

        bt_dossier = Button(self, text="Indiquer le dossier départ", command=partial(self.jopen_dossier, 1)) #command=self.jopen_dossier)
        bt_dossier.grid(row=2, column=0, padx=10, pady=10)

        self.box_dossier = Entry(self, width=80)
        self.box_dossier.grid(row=2, column=1, padx=30, pady=10)

        # bt_repso = Button(self, text="Repertoire sortie fichier xlsx", command=partial(self.jopen_dossier, 2)) #command=self.jopen_rep)
        # bt_repso.grid(row=4, column=0, padx=10, pady=10)
        #
        # self.box_repso = Entry(self, width=80)
        # self.box_repso.grid(row=4, column=1, padx=10, pady=10)

        bt_exe = Button(self, text="Exécuter", command=self.executer, fg="red", font="Verdana 10 bold")
        bt_exe.grid(row=4, column=1, sticky=W, padx=120, pady=10)

        bt_fer = Button(self, text="Fermer", command=self.destroy, width=5, height=1)
        bt_fer.grid(row=4, column=1, sticky=W, padx=220, pady=10)


        # attribut

        self.dos_dep = ''

    # pour test
    #     self.box_dossier.insert(0, "E:/Python/Projet_3_4/Prepare250KDiffusion/exDonnee/Pente_250k")


    def jopen_dossier(self, option):
        try:
            repnom = filedialog.askdirectory(title="Indiquer le repertoire de départ")
        except NameError:
            repnom = filedialog.askdirectory(title="Indiquer le repertoire de départ", initialdir="")

        # if option == 1:
        self.box_dossier.delete(0, END)
        self.box_dossier.insert(0, repnom)

        # if option == 2:
        #     self.box_repso.delete(0, END)
        #     self.box_repso.insert(0, repnom)



    def executer(self):

        try:
            self.prep250k.execute(self.box_dossier.get())

        except Exception as e:
            messagebox.showerror("Erreur", "Le traitement a rencontré un problème. Veuillez vous assurer que les chemins ne comporte pas d'espace. "
                                           "Sinon veuillez consulter le support technique.")
            raise






