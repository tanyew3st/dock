from __future__ import print_function
import os
import flask
from ml import MachineLearning
from protein import Protein
import numpy as np
import pandas as pd

# selected by the user upon initial interaction with the API
proteinToUse = "EFRR"

# needs to be added by user
ligand = "actives_final_1.pdbqt"

affinityScores = {}

directory = None

proteins = []

affinityScoresTest = {

}


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

# Main method
if __name__ == "__main__":

    ml = MachineLearning(affinityScoresTest)
    MachineLearning.createDirectory("/Users/tchandak/Desktop/Dock/dock/Actives", None, None)












    # this will be done in the front end just taking user input to find the protein they want to use
    proteinToUse = str.upper(raw_input("Protein to dock to: "))

    # searching through the proteins directory to find the protein the user wants to dock to
    for i in os.listdir("proteins"):
        if i == proteinToUse:
            directory = "proteins/" + i + "/Structures"
    if directory is None:
        print("Couldn't find directory")

        # should return to the API with null or something if the protein files don't exist
        exit(0)

    # now searching through and creating protein array
    for i in os.listdir(directory):

        # directory for the conf.txt
        prtdir = directory + "/" + i + "/conf.txt"

        # if to get rid of .ds-store and other weird files
        if len(i) <= 4:
            p1 = Protein(prtdir, directory + "/" + i + "/", i)
            proteins.append(p1)

    print(*proteins, sep='\n')


    # docking. this could be part of the earlier file
    for i in proteins:
        dock(i)

    # now I am ready to run the machine learning model
    """
     docking example {
        "1M14": -4.5
        "1XKK": -8.9
        "2EB2": -9.3
        etc.
    """

