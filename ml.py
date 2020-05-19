import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression;


class MachineLearning:
    affinity = None
    prob = {}

    def __init__(self, testaffinity):
        self.affinity = testaffinity

    # input is the location of the folder of the pdbqt files
    # output is where it will be printed to
    # boolean active to add ticker 1 or 0 to the excel spreadsheet
    @staticmethod
    def createDirectory(inputdir, outputdir, active):
        columns = []
        for i in os.listdir(inputdir):
            columns.append(i[0:4])
        beginning = True
        maximum = 0

        missingData = []
        for i in os.listdir(inputdir):
            dictionary = {}

            opened = open(inputdir + "/" + i, encoding="unicode_escape").readlines()

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
                df = pd.DataFrame(index=np.arange(1, maximum + 1), columns=columns)

            for k in range(1, maximum + 1):
                try:
                    int(i[0])
                    str(i[1])
                except ValueError:
                    continue
                if k in dictionary:
                    df.at[k, i[0:4]] = float(dictionary[k])
                else:
                    missingData.append([k, i[0:4]])
            beginning = False
        df.dropna()


        # drop columns that we dont need`
        # missing data is extremely weird and fix it
        df = df.reindex(sorted(df.columns), axis=1)

        for i in df.columns:
            try:
                int(i[0])
                str(i[1])
            except ValueError:
                del df[i]

            
        print(df)

        print(missingData)


        # if active:
        #     df.to_excel(outputdir + "/active.xlsx")
        # else:
        #     df.to_excel(outputdir + "/decoy.xlsx")
        print("finished")
        # end product to create a new excel spreadsheet .xlsx in the output location

    def getProbability(self, activePath, decoyPath):
        actives = pd.read_excel(activePath, index=False)
        actives.drop("Unnamed: 0", axis=1, inplace=True)
        active_ticker = np.ones(len(actives))
        print('ACTIVES')

        decoys = pd.read_excel(decoyPath, index=False)
        decoys.drop("Unnamed: 0", axis=1, inplace=True)
        decoy_ticker = np.zeros(len(decoys))
        print('DECOYS')

        all_vals = pd.concat([actives, decoys], ignore_index=True)
        all_ticker = np.concatenate([active_ticker, decoy_ticker])

        print(all_vals)
        print(all_ticker)

        # X_train, X_test, y_train, y_test = train_test_split(all_vals, all_ticker, test_size=0.33, random_state=50)

        logModel = LogisticRegression()
        logModel.fit(all_vals, all_ticker)

        predictions = logModel.predict(self.affinity)
        print(predictions)
