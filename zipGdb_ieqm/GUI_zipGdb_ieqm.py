

from tkinter import Tk, Button, Label, Entry, E, W,END, filedialog, Checkbutton, IntVar, Radiobutton

# from tkFileDialog import askopenfilename, askdirectory

from tkinter import messagebox
from functools import partial
from domaine.zipGdb_ieqm import ZipGdb_ieqm


class App_zippGdb_optSqlite(Tk):
    # Application developper pour ...
    # auteur - date
    # Exemple utilité, zipper les GDB au 250K creé pour le telechargement des IEQM peuplements dans IGO et donnée Québec
    # pour DondroLidar on convertie aussi, les 2 formats sont disponible pour téléchargement


    def __init__(self):

        Tk.__init__(self)

        self.version = 1
        self.geometry("760x270+600+250")
        self.title("Outil de zippage de gdb IEQM Version: {}".format(self.version))
        self.objZip = None

        self.dos_depart = ''
        self.dos_sortie = ''

        self.enTest = False


        # Widget

        self.etiquette = Label(self, text="Indiquer comme dossier de départ le répertoire de sortie de l'outil découpage qui produit\nles gdb 93 et 10. (carte ORI et MAJ)"
                                 " Le traitement prend environ 30 secondes par fichier.")
        self.etiquette.grid(row=1,column=1, padx=10, pady=10, sticky=W)

        # self.valConversionCheck = IntVar()
        # self.checkConversion = Checkbutton(self, text="Faire aussi la\nconversion en SQLITE", variable=self.valConversionCheck)
        # self.checkConversion.grid(row=2, column=0, sticky='')

        self.valEcraseCheck = IntVar()
        self.valEcraseCheck.set(1)
        self.checkEcrase = Checkbutton(self, text="Écraser les zip\ndans les répertoires de sortie", variable=self.valEcraseCheck)
        self.checkEcrase.grid(row=1, column=0, sticky=W, padx=15)


        self.type = IntVar()
        self.type.set(1)

        radio_ori = Radiobutton(self, text="Zip gdb ORI", variable=self.type, value=1,  command=self.setEtiquette)
        radio_maj = Radiobutton(self, text="Zip gdb MAJ", variable=self.type, value=2, command=self.setEtiquette)
        radio_dendroLid = Radiobutton(self, text="Conversion SQLITE et zip \ngdb dendro_lidar", variable=self.type, value=3, command=self.setEtiquette)
        # radio_conversion = Radiobutton(self, text="Validation et\nConversion ACQ", variable=self.type_vp, value=4)
        # radio_correction = Radiobutton(self, text="Officialisation\nCorrections", variable=self.type_vp, value=5)


        radio_ori.grid(row=2, column=0, sticky=W, pady=10, padx=10)
        radio_maj.grid(row=2, column=1, sticky=W, pady=10, padx=10)
        radio_dendroLid.grid(row=2, column=1, sticky=W, pady=10, padx=200)


        # self.valMajCheck = IntVar()
        # self.checkMaj = Checkbutton(self, text="Faire sur gdb MAJ", variable=self.valMajCheck)
        # self.checkMaj.grid(row=2, column=1, sticky=W, padx=20)


        self.bt_dossier = Button(self, text="Indiquer le dossier départ", command=partial(self.jopen_dossier, 1)) #command=self.jopen_dossier)
        self.bt_dossier.grid(row=3, column=0, padx=10, pady=10)

        self.box_dosDepart = Entry(self, width=80)
        self.box_dosDepart.grid(row=3, column=1, padx=30, pady=10)

        self.bt_dosSortie = Button(self, text="Repertoire sortie des fichiers zip", command=partial(self.jopen_dossier, 2)) #command=self.jopen_rep)
        self.bt_dosSortie.grid(row=4, column=0, padx=10, pady=10)

        self.box_dosSortie = Entry(self, width=80)
        self.box_dosSortie.grid(row=4, column=1, padx=10, pady=10)

        bt_exe = Button(self, text="Exécuter", command=self.executer, fg="red", font="Verdana 10 bold")
        bt_exe.grid(row=6, column=1, sticky=W, padx=80, pady=10)

        bt_fer = Button(self, text="Fermer", command=self.destroy, width=5, height=1)
        bt_fer.grid(row=6, column=1, sticky=W, padx=180, pady=10)


################################
        if self.enTest:

            self.box_dosDepart.insert(0, 'E:/Python/Projet_3_4/zippGdb_optConversionSqlite/exempleDonnee/Carte_maj/Avant')
            self.box_dosSortie.insert(0, 'E:/Python/Projet_3_4/zippGdb_optConversionSqlite/exempleDonnee/Carte_maj/sortiOutil')
            # self.valConversionCheck.set(1)


    # pour test
    #     self.box_dossier.insert(0, "E:/Python/Projet_3_4/Prepare250KDiffusion/exDonnee/Pente_250k")
    def setEtiquette(self):

        if self.type.get() == 1:
            self.etiquette.config(text="Indiquer comme dossier de départ le répertoire de sortie de l'outil découpage qui produit\n"
                                       "les gdb 93 et 10."
                                 " Le traitement prend environ 30 secondes par fichier.")
            self.box_dosSortie.config(state='normal')
            self.bt_dosSortie.config(state="normal")

        if self.type.get() == 2:
            self.etiquette.config(text="Indiquer comme dossier de départ le répertoire de sortie de l'outil découpage qui produit\n"
                                       "les gdb 93 et 10.\n"
                                "NB: Pour maj, le nom de la gdb sera modifiée pour CARTE_ECO_MAJ_xxx_yy")
            self.box_dosSortie.config(state='normal')
            self.bt_dosSortie.config(state="normal")

        if self.type.get() == 3:
            self.etiquette.config(text="Indiquer comme dossier de départ le répertoire qui contient les 250K.\n"
                                "NB: Pour le Dendro lidar, les fichiers en sortie (SQL et GDB zipper) seront dans\n le même répertoire que le rep départ")

            self.box_dosSortie.config(state='disabled')
            self.bt_dosSortie.config(state="disabled")

    def jopen_dossier(self, option):
        try:
            repnom = filedialog.askdirectory(title="Indiquer le repertoire de départ")
        except NameError:
            repnom = filedialog.askdirectory(title="Indiquer le repertoire de départ", initialdir="")

        if option == 1:
            self.box_dosDepart.delete(0, END)
            self.box_dosDepart.insert(0, repnom)

        if option == 2:
            self.box_dosSortie.delete(0, END)
            self.box_dosSortie.insert(0, repnom)


    def executer(self):

        try:

            self.dos_depart = self.box_dosDepart.get()
            self.dos_sortie = self.box_dosSortie.get()

            maj, ecrase = None, None
            # if self.valConversionCheck.get() == 1:
            #     conversionSqlite = True
            # else:
            #     conversionSqlite = False

            if self.valEcraseCheck.get() == 1:
                ecrase = True
            else:
                ecrase = False

            leType = ''
            if self.type.get() == 1:
                leType = "ori"

            elif self.type.get() == 2:
                leType = "maj"

            elif self.type.get() == 3:
                leType = "dendroLid"

            self.objZip = ZipGdb_ieqm(self.dos_depart, self.dos_sortie, ecrase, leType)
            self.objZip.execute()



        except Exception as e:
            messagebox.showerror("Erreur", "Le traitement a rencontré un problème. Veuillez vous assurer que les chemins ne comporte pas d'espace. "
                                           "Sinon veuillez consulter le support technique.")
            self.destroy()
            raise






