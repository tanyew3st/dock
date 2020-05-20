from __future__ import print_function
import os
import shutil

import flask
from ml import MachineLearning
from protein import Protein
import numpy as np
import pandas as pd
import xlrd

# selected by the user upon initial interaction with the API
proteinToUse = "EGFR"

# Configurations for Flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# needs to be added by user
ligand = "actives_final_1.pdbqt"

affinityScores = ["1M14", "1XKK", "2EB2", "2EB3",    "2GS2",    "2GS7",    "2ITN",    "2ITT",    "2J5F",    "2JIT",    "2JIU",    "2RGP",    "3BEL",
                  "3IKA",    "3UG1",    "3VJO",    "4G5J",    "4G5P",    "4I23",    "4I24",    "4JQ7",    "4LI5",    "4LL0",    "4LQM",    "4LRM",   "4RIW",
                  "4TKS",    "4ZJV",    "5CAV",    "5CNN",    "5FED",    "5FEE",    "5XDL",    "5Y9T",    "outp"]
ascores = [-6.8,-8.2,-7.1,-7.6,-7.0,-8.4,-7.1,-7.3,-7.5,-8.2,-8.0,-8.1,-9.1,-7.5,-6.9,-7.1,-7.8,-8.1,-7.4,-9.1,-7.8,-8.1,-8.9,-8.1,-8.6,-7.6,-7.4,-8.4,-7.6,-8.0,-7.1,-7.6,-6.9,-7.7]

directory = None

proteins = []

affinityScoresTest = {'1M14': -6.8, '1XKK': -8.2, '2EB2': -7.1, '2EB3': -7.6,
     '2GS2': -7.0, '2GS7': -8.4, '2ITN': -7.1, '2ITT': -7.3,
     '2J5F': -7.5, '2JIT': -8.2, '2JIU': -8.0, '2RGP': -8.1,
     '3BEL': -9.1, '3IKA': -7.5, '3UG1': -6.9, '3VJO': -7.1,
     '4G5J': -7.8, '4G5P': -8.1, '4I23': -7.4, '4I24': -9.1,
     '4JQ7': -7.8, '4LI5': -8.1, '4LL0': -8.9, '4LQM': -8.1,
     '4LRM': -8.6, '4RIW': -7.6, '4TKS': -7.4, '4ZJV': -8.4,
     '5CAV': -7.6, '5CNN': -8.0, '5FED': -7.1, '5FEE': -7.6,
     '5XDL': -6.9, '5Y9T': -7.7}

# provide prediction object with predictions given only affinity numbers
def getPredWithAffinity(protein, affinity):
    print("getting predictions with affinity numbers")

# @app.route('/', methods=['GET'])
# def sayHello():
#     return "Hello World!!"

def makeFolders(path):
    os.mkdir(path + "/Actives")
    os.mkdir(path + "/Decoy")
    for folder in os.listdir(path):
        if folder.__contains__("active"):
            shutil.move(folder, folder + "/Actives")

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
    # app.run()

    # ml = MachineLearning(affinityScoresTest)
    # MachineLearning.createDirectory("/Users/tchandak/Desktop/STARS Data/Decoys", "proteins/EGFR", False)
    # exit(52)
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

    # print(*proteins, sep='\n')

    # docking. this could be part of the earlier file
    # for i in proteins:
    #     dock(i)

    # now I am ready to run the machine learning model
    """
     docking example {
        "1M14": -4.5
        "1XKK": -8.9
        "2EB2": -9.3
        etc.
    """
    driver = MachineLearning(affinityScoresTest)
    driver.getProbability("/Users/tchandak/Desktop/Dock/dock/proteins/EGFR/active.xlsx", "/Users/tchandak/Desktop/Dock/dock/proteins/EGFR/decoy.xlsx")
