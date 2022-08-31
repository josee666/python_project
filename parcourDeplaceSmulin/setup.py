from distutils.core import setup
import sys, os, shutil, py2exe
import py2exe
# cwd = os.path.dirname(os.path.realpath(__file__))
# print cwd
# sys.path.append(os.path.join(cwd, "prerequis"))

## Copier le module commun interaction DB dans prerequis
# cwd = os.path.join(cwd, "prerequis").replace("\\", "/")
# shutil.copy2("//Sef1271a/F1271g/OutilsProdDIF/modules_communs/python27/InteractionDB/bin/InteractionDB.pyc", cwd)  # "//Sef1271a/F1271g/OutilsProdDIF/modules_communs/python27/InteractionDB
# # shutil.copy2('E:/Python/module_commun/InteractionDB.py', cwd)  # "//Sef1271a/F1271g/OutilsProdDIF/modules_communs/python27/InteractionDB
#

# data_file = [('', [r'sous_ensemble.ico'])]
#
# setup(windows=[{"script": 'Creation_sous_ensemble_MDB.py', "icon_resources": [(0, "sous_ensemble.ico")]}], data_files=data_file,
#     options={"py2exe": {"includes": "datetime, Tkinter, tkFileDialog, Tkconstants, sys, os, time,distutils.core, pyodbc, shutil, tkMessageBox, math" } }
#
# )

setup(
    zipfile=None,
    windows=[{"script": "gui_smullinParcourDeplace.py",  ### Main Python script
    "icon_resources": [(0, "double_arrow.ico")],
    # "dist_dir": "distribution_VP", ## marche pas
    "dest_base": "Deplace_Smullin"}],  # )
    options={"py2exe":{
        "excludes":["tests"]}})

#   python setup.py py2exe install
