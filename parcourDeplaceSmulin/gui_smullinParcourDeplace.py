

# -*- coding: utf-8 -*-
import os
import shutil
import time
import getpass

from tkinter import Tk, Button, Label, Entry, E, W,END, filedialog, messagebox, Radiobutton, IntVar, END, ACTIVE, DISABLED

from tkinter.filedialog import askopenfilename, askdirectory
#
from functools import partial
from domaine.rechercheDansArboSmullin import *


class App_smullinDeplace(Tk):
    # Application developper pour ...
    # auteur - date

    def __init__(self):

        Tk.__init__(self)

        self.version = 000
        self.geometry("780x250+500+100")
        self.title("Preparation des déplacements des fichiers sur Smullin non-public. Version: {}".format(self.version))
        self.arboSmullin = None

        # Widget

        self.type_app = IntVar()
        self.type_app.set(1)


        self.label1 = Label(self, text="Le repertoire de départ est: Smullin/lidar/FORET/PRODUITS_DERIVES/Projet_Provincial")
        self.label1.grid(row=0,column=0, columnspan=2, padx=10,pady=10, sticky=W)

        self.label2 = Label(self, text="Le repertoire de déplacement est: Smullin/lidar/public")
        self.label2.grid(row=1,columnspan=2, padx=10, sticky=W)

        self.labelMessage = Label(self, text="", fg="blue", font=("Helvetica", 11))
        self.labelMessage.grid(row=1,column=1,pady=10, sticky=W)

        radio_parcour = Radiobutton(self, text="Créer rapport de vérification Smullin", variable=self.type_app, value=1)
        radio_deplace = Radiobutton(self, text="Déplacer les fichiers", variable=self.type_app, value=2)

        radio_parcour.grid(row=2, columnspan=3, sticky=W, padx=50)
        if getpass.getuser().upper() in ["LEMMAB", "MARJO3"]:
            radio_deplace.grid(row=2, columnspan=3, sticky=W, padx=300)

        bt_dossierSortie = Button(self, text="Indiquer le dossier de sortie du rapport", command=partial(self.jopen_dossier, 1)) #command=self.jopen_dossier)
        bt_dossierSortie.grid(row=3, column=0, padx=10, pady=10)

        self.box_dossierSortie = Entry(self, width=80)
        self.box_dossierSortie.grid(row=3, column=1, padx=30, pady=10)


        self.bt_exe = Button(self, text="Exécuter", command=self.executer, fg="red", font="Verdana 10 bold")
        self.bt_exe.grid(row=4, column=1, sticky=W, padx=30, pady=30)

        self.bt_fer = Button(self, text="Fermer", command=self.destroy, width=5, height=1)
        self.bt_fer.grid(row=4, column=1, sticky=W, padx=130, pady=30)


        # attribut
        self.dos_dep = ''

        # pour test
        # self.box_dossierSortie.insert(0, "E:/a_temp/lidarTest")
        # self.box_dossierSortie.insert(0, "S:/FORET/PRODUITS_DERIVES/Projet_Provincial")

        self.mainloop()


    def jopen_dossier(self, option):
        try:
            repnom = filedialog.askdirectory(title="Indiquer le repertoire de sortie")
        except NameError:
            repnom = filedialog.askdirectory(title="Indiquer le repertoire de sortie", initialdir="")

        # if option == 1:
        self.box_dossierSortie.delete(0, END)
        self.box_dossierSortie.insert(0, repnom)


    def reactive(self, reactive):
        """ param pour mettre active ou desactive
        """
        if reactive:
            self.labelMessage["text"] = ""
            self.bt_exe['state'] = ACTIVE
            self.bt_fer['state'] = ACTIVE
            self.labelMessage["text"] = "Traitement terminé veuillez consulter le fichier rapport:\n {} ".format(self.box_dossierSortie.get() + "/SmullinRecherche_date.xlsx")

        elif reactive == False:
            self.label1["text"] = ""
            self.label2["text"] = ""
            self.label2["state"] = DISABLED

            self.labelMessage["text"] = "Traitement en cour, veuillez patienter..."

            self.bt_exe['state'] = DISABLED
            self.bt_fer['state'] = DISABLED


    def executer(self):

        try:

            temps_debut = time.time()

            self.reactive(False)
            #
            # self.labelMessage["text"] = "Validation en cour, veuillez patienter..."
            # self.bt_exe['state'] = DISABLED
            # self.bt_fer['state'] = DISABLED
            messagebox.showinfo("DEBUT", "Début du traitement")


            self.dos_dep = self.box_dossierSortie.get()
            self.arboSmullin = RechercheDansArboSmullin(self.dos_dep)

            # self.type_app.get()
            if self.type_app.get() == 2:
                self.arboSmullin.parcourArbo(deplace=True)
            else:
                self.arboSmullin.parcourArbo(deplace=False)


            try:
                self.arboSmullin.workbook.close()
            except:
                pass

            elapsed = round((time.time() - temps_debut) / 60, 2)

            messagebox.showinfo('Fin', "Traitement terminé. Temps exécution: {} ".format(elapsed))
            self.reactive(True)



        except Exception as e:
            messagebox.showerror("Erreur", "Le traitement a rencontré un problème. Veuillez vous assurer que les chemins ne comporte pas d'espace. "
                                           "Sinon veuillez consulter le support technique.")

            try:
                self.arboSmullin.workbook.close()
            except:
                pass

            raise



if __name__ == '__main__':

    app = App_smullinDeplace()






