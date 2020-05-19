from __future__ import print_function
import os
from protein import Protein

# selected by the user upon initial interaction with the API
protein = "EGFR"

# needs to be added by user
ligand = "actives_final_1.pdbqt"

directory = None

proteins = []

def dock(protein):
    command = "./vina "
    command += "--ligand " + ligand + " "
    for i in protein.properties:
        command += "--" + i + " " + protein.properties[i] + " "

    os.system(command)


    print(command)
if __name__ == "__main__":
    # command = "./vina"
    # os.system(command)

    for i in os.listdir("proteins"):
        directory = "proteins/" + i

    for i in os.listdir(directory):
        # directory for the conf.txt
        prtdir = directory + "/" + i + "/conf.txt"

        # if to get rid of .ds-store and other weird files
        if len(i) <= 4:
            p1 = Protein(prtdir, directory + "/" + i + "/")
            proteins.append(p1)

    print(*proteins,sep='\n')

    for i in proteins:
        dock(i)