from __future__ import print_function
import os
from protein import Protein
from subprocess import Popen, PIPE


# selected by the user upon initial interaction with the API
protein = "EGFR"

# needs to be added by user
ligand = "actives_final_1.pdbqt"

affinityScores = {}

directory = None

proteins = []

def dock(protein):
    print(protein.structure)
    affinityScores[protein.structure] = -7.3
    command = "./vina "
    command += "--ligand " + ligand + " "

    for i in protein.properties:
        command += "--" + i + " " + protein.properties[i] + " "

    console = os.popen(command).read().split(' ')
    print(console)

    newArray = []

    for i in console:

        try:
            newArray.append(float(i))
            newArray.append(int(i))
        except:
            print(i + " is not an int")

    print(protein.structure)

    obj = {protein.structure: min(newArray)}
    affinityScores.update(obj)

if __name__ == "__main__":

    # list_of_ls = os.popen("./vina --config conf.txt").read().split(' ')

    # os.system("./vina")
    # command = "./vina"
    # os.system(command)

    for i in os.listdir("proteins"):
        directory = "proteins/" + i

    for i in os.listdir(directory):
        # directory for the conf.txt
        prtdir = directory + "/" + i + "/conf.txt"

        # if to get rid of .ds-store and other weird files
        if len(i) <= 4:
            p1 = Protein(prtdir, directory + "/" + i + "/", i)
            proteins.append(p1)

    print(*proteins,sep='\n')

    for i in proteins:
        dock(i)