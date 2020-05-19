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
            print(i)
            columns.append(i)
        beginning = True
        maximum = 0

        for i in os.listdir(inputdir):
            dictionary = {}

            opened = open(inputdir + "/" + i).readlines()

            for items in opened:
                if items.__contains__("Found"):
                    continue
                num = ''

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
                df = pd.dataFrame(index=np.arange(maximum + 1), columns=columns)

            for k in range(1, maximum + 1):
                df.set_value(k, i, dictionary[k])
            beginning = False
        print(df)
        # end product to create a new excel spreadsheet .xlsx in the output location
