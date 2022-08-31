
# -*- coding: utf-8 -*-

from tkinter import Tk, Label, Button, Entry, E, W, IntVar, Radiobutton, END, ACTIVE, DISABLED
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, askdirectory
from datetime import datetime
from domaine.rechercheDansArbo import RechercheDansArbo

from functools import partial
import getpass
import time
import os


def date_actuelle():
    """ Fonction qui retourne l'annee du systeme
    Exemple: 2017_12_01 """
    date_time = datetime.now()
    date_format = date_time.strftime("%Y_%m_%d %Hh%Mmin%Ssec")

    return date_format[:10]


class App_rechercheDossier_gui(Tk):
    # Application developper pour rechercher/supprimer des dossier et leur contenu à partir d'un repertoire
    # JM 2018-03-01

    def __init__(self):

        Tk.__init__(self)

        self.geometry("930x300+450+100")
        self.title("Recherche de dossier à partir d'un répertoire")
        self.version = 1
        self.userName = getpass.getuser()
        # self.userName = "sfsdg"


        # Widget
        label = Label(self, text="Recherche de dossier à partir d'un répertoire", font="Verdana 8")
        label.grid(row=0, columnspan=2, pady=10)


        self.type_app = IntVar()
        self.type_app.set(1)

        radio_recherche = Radiobutton(self, text="Recherche dossier", variable=self.type_app, value=1)
        radio_supprime = Radiobutton(self, text="Suppression", variable=self.type_app, value=2)

        radio_recherche.grid(row=1, column=1, sticky=W, pady=10, padx=10)

        if self.userName in ["marjo3"]:
            radio_supprime.grid(row=1, column=1, sticky=W, pady=10, padx=170)


        bt_dossier = Button(self, text="Indiquer dossier départ de la recherche", command=partial(self.jopen_dossier, 1)) #command=self.jopen_dossier)
        bt_dossier.grid(row=2, column=0, padx=10, pady=10, sticky=W+E)

        self.box_dossierDepart = Entry(self, width=110)
        self.box_dossierDepart.grid(row=2, column=1, sticky=W, padx=10, pady=10)

        bt_choix_fichier = Button(self, text="Fichier des dossiers a rechercher", command=self.jopencouche)
        bt_choix_fichier.grid(row=3, column=0, padx=10, pady=10, sticky=W+E)

        self.box_fil = Entry(self, width=110)
        self.box_fil.grid(row=3, column=1, padx=10, pady=10,sticky=W)

        bt_repso = Button(self, text="Repertoire sortie fichier xlsx", command=partial(self.jopen_dossier, 2)) #command=self.jopen_rep)
        bt_repso.grid(row=4, column=0, padx=10, pady=10)

        self.box_repSortie = Entry(self, width=110)
        self.box_repSortie.grid(row=4, column=1, padx=10, pady=10, sticky=W)

        self.label_message = Label(self, text="", foreground="blue")
        self.label_message.grid(row=5, columnspan=2, padx=30)

        self.bt_exe = Button(self, text="Exécuter", command=self.executer, fg="red", font="Verdana 10 bold")
        self.bt_exe.grid(row=6, column=1, sticky=W, padx=120, pady=20)

        self.bt_fer = Button(self, text="Fermer", command=self.destroy, width=5, height=1)
        self.bt_fer.grid(row=6, column=1, sticky=W, padx=220, pady=20)


        # attribut

        self.dosDep = ''
        self.path_fil = ''
        self.dosSortie = ''
        self.objRechercheDos = ''

        ####
        # ############
        # TEST
        #########
        # self.box_repSortie.insert(0, 'E:/Python/Projet_3_4/DG_chercheFichier/sortie')
        # self.box_dossierDepart.insert(0, 'E:/a_temp')
        # self.box_fil.insert(0, 'E:/Python/Projet_3_4/DG_chercheFichier/MCE.txt')
        ################


        self.mainloop()

    def reactive(self):
        self.label_message["text"] = ""
        self.bt_exe['state'] = ACTIVE
        self.bt_fer['state'] = ACTIVE


    def jopencouche(self):

        couche = askopenfilename(title="Pointer le fichier contenant les dossiers a rechercher", filetypes=[('TEXT Files', '*.txt')])

        self.box_fil.delete(0, END)
        self.box_fil.insert(0, couche)


    def jopen_dossier(self, option):

        repnom = askdirectory(title="Indiquer le répertoire", initialdir="")

        if option == 1:
            self.box_dossierDepart.delete(0, END)
            self.box_dossierDepart.insert(0, repnom)

        if option == 2:
            self.box_repSortie.delete(0, END)
            self.box_repSortie.insert(0, repnom)


    def executer(self):

        try:

            temps_debut = time.time()

            self.label_message["text"] = "Validation en cour, veuillez patienter..."
            self.bt_exe['state'] = DISABLED
            self.bt_fer['state'] = DISABLED
            messagebox.showinfo("DEBUT", "Début de la validation!")


            self.dosDep = self.box_dossierDepart.get()
            self.path_fil = self.box_fil.get()
            self.dosSortie = self.box_repSortie.get()

            ###############
            #   verif les path
            ############

            if not os.path.isfile(self.path_fil):
                messagebox.showerror('', "{} n'est pas un fichier, veuillez indiquer un fichier".format(self.path_fil))
                self.reactive()
                return
            if not os.path.isdir(self.dosDep) :
                messagebox.showerror('', "Le dossier de départ indiqué est incorrect")
                self.reactive()
                return
            if not os.path.isdir(self.dosSortie) :
                messagebox.showerror('', "Le dossier de sortie indiqué est incorrect")
                self.reactive()
                return


            ############
            # lire le fichier pointer par utilisateur
            ############
            monFil = open(self.path_fil, "r")

            contenue = monFil.read()
            listContenue = contenue.split()

            monFil.close()

            #############
            # parcour arborescence
            ##############
            self.objRechercheDos = RechercheDansArbo(dosDepart=self.dosDep, listDossierARecherche=listContenue, dosFichierSortie=self.dosSortie)
            self.objRechercheDos.parcourArbo()

            self.objRechercheDos.gestionListNonTrouve()


            try:
                self.objRechercheDos.workbook.close()
                print('ok close')

            except IOError as e:
                raise Exception("Le fichier .XLSX est ouvert par une autre application, veuillez le fermer et relancer l'application")

            elapsed = round((time.time() - temps_debut) / 60, 2)
            messagebox.showinfo('Fin', "Traitement terminé. Temps exécution: {} ".format(elapsed))
            self.reactive()
            # self.destroy()


        except Exception as e:

            try:
                messagebox.showerror('Fin', "Une erreur est survenue: {}, veuillez consulter le support technique".format(e))
            except:
                messagebox.showerror('Fin', "Une erreur est survenue, veuillez consulter le support technique")

            self.destroy()



if __name__ == '__main__':
    app = App_rechercheDossier_gui()
