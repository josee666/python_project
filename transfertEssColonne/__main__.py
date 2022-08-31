from transfertEss_gui import *

try:

    app = App_transfertEssence()
    app.mainloop()


except Exception as e:
    tkMessageBox.showerror("problème", "L'outil a rencontré un probleme, veuillez consulter le support technique")
    #                                                     "déposer l'outil dans un autre emplacement".format(os.getcwd()))
    print('PROBLEME')
    raise