import os
import shutil, py2exe
from distutils.core import setup

cwd = os.path.dirname(os.path.realpath(__file__))

rep_doc = "E:/Python/Projet_3_4/zipGdb_ieqm/Documentation_outil_zippage_GDB_ieqm.docx"
rep_doc_dist = "E:/Python/Projet_3_4/zipGdb_ieqm/dist/Documentation_outil_zippage_GDB_ieqm.docx"


if os.path.exists(rep_doc_dist):
    os.remove(rep_doc_dist)
shutil.copy(rep_doc, rep_doc_dist)


setup(
    zipfile=None,
    windows=[{"script": "__main__.py",  ### Main Python script
    "icon_resources": [(1, "fleche.ico")],
    # "dist_dir": "distribution_VP", ## marche pas
    "dest_base": "zip_Gdb_ieqm"}],   #)
    options={"py2exe":{
        "excludes":["tests"]}})

#   python setup.py py2exe install

# setup(
#     zipfile=None,
#     windows=[{"script": "Creation_sous_ensemble_MDB.py",  ### Main Python script
#     "icon_resources": [(0, "tes.ico")],
#     # "dist_dir": "distribution_VP", ## marche pas
#     "dest_base": "Creation_sous_ensemble_MDB"}],  # )
#     options={"py2exe":{
#         "excludes":["tests"]}})



#test
# ico_file = 'D:\\Mes documents\\icones\\pythonmat.ico'
#
# setup(
#     console=[
#         dict(
#             script = '__main__.py',
#             dest_base= "Valide_Peuplements",
#             icon_resources = [(1, ico_file)]
#             )
#     ],
#     data_files = ['init.py']
#
# )