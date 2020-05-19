import pandas as pd
import numpy as np
import os

class MachineLearning:
    affinity = None

    def __init__(self, affinity):
        self.affinity = affinity

    # input is the location of the folder of the pdbqt files
    # output is where it will be printed to
    # boolean active to add ticker 1 or 0 to the excel spreadsheet
    @staticmethod
    def createDirectory(inputdir, outputdir, active):
        columns = []
        for i in os.listdir(inputdir):
            print(i[0:4])
            columns.append(i[0:4])
        beginning = True
        maximum = 0

        missingData = []
        for i in os.listdir(inputdir):
            dictionary = {}

            opened = open(inputdir + "/" + i).readlines()

            for items in opened:
                if items.__contains__("Found"):
                    continue
                num = ''
                if items[0] != '-':
                    break
                for j in items.split()[1].split('_')[2]:
                    if j != '/':
                        num += j
                    else:
                        break
                if beginning:
                    if int(num) > maximum:
                        maximum = int(num)
                dictionary[int(num)] = float(items.split()[0])
            if beginning:
                df = pd.DataFrame(index=np.arange(1,maximum + 1), columns=columns)

            for k in range(1, maximum + 1):
                if k in dictionary:
                    df.at[k, i[0:4]] = float(dictionary[k])
                else:
                    missingData.append([k,i[0:4]])
            
            beginning = False
        df.dropna()
        print(df)
        print(missingData)
        # end product to create a new excel spreadsheet .xlsx in the output location
