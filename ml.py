import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier;
from sklearn.ensemble import RandomForestClassifier;
from sklearn.svm import SVC

# class to provide Machine Learning and create a model
class MachineLearning:
    # results should contain prob object
    # and affinity object
    results = {}

    # affinity scores made in the constructor
    affinity = None

    # probability object that contains all the probabilities for the various models
    prob = {}

    # on init set the affinity array equal to the affinity scores provided by vina
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

            # opened = open(inputdir + "/" + i, encoding="unicode_escape").readlines()
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

        for i in df.columns:
            try:
                int(i[0])
                str(i[1])
            except ValueError:
                del df[i]

        df.dropna(inplace=True)
        print(df)

        if active:
            df.to_excel(outputdir + "/active.xlsx")
        else:
            df.to_excel(outputdir + "/decoy.xlsx")
        print("finished")
        # end product to create a new excel spreadsheet .xlsx in the output location

    # gets the probability using various machine learning models and sets
    def getProbability(self, activePath, decoyPath):
        # reading the active files from the excel spreadsheet
        actives = pd.read_excel(activePath, index=False)
        actives.drop("Unnamed: 0", axis=1, inplace=True)
        active_ticker = np.ones(len(actives))
        print('ACTIVES')

        # reading the decoy files from the excel spreadsheet
        decoys = pd.read_excel(decoyPath, index=False)
        decoys.drop("Unnamed: 0", axis=1, inplace=True)
        decoy_ticker = np.zeros(len(decoys))
        print('DECOYS')

        # creating all the values
        all_vals = pd.concat([actives, decoys], ignore_index=True)

        # assigning 0 or 1 if it is active (1) or decoy (0)
        all_ticker = np.concatenate([active_ticker, decoy_ticker])

        print(all_vals)
        # X_train, X_test, y_train, y_test = train_test_split(all_vals, all_ticker, test_size=0.33, random_state=50)
        if all_vals.isnull().values.any():
            print(pd.isnull(all_vals).any(1).nonzero()[0])
            exit(4)

        y = pd.DataFrame(self.affinity, index=[0])

        # Logistic Regression
        print "Doing Logistic Regression"
        logModel = LogisticRegression()
        logModel.fit(all_vals, all_ticker)
        plr = logModel.predict_proba(y)
        self.prob["lr"] = plr

        # K Nearest Neighbors
        print "Doing KNN"
        knn = KNeighborsClassifier(n_neighbors=100)
        knn.fit(all_vals, all_ticker)
        pknn = knn.predict_proba(y)
        self.prob["knn"] = pknn

        # Support Vector Machines
        print "Doing Support Vector Machines"
        svc = SVC(C=100, gamma=0.2, probability=True)
        svc.fit(all_vals, all_ticker)
        psvc = svc.predict_proba(y)
        self.prob["svc"] = psvc

        # Random Forest
        print "Doing Random Forest Classifier"
        rf = RandomForestClassifier(n_estimators=750)
        rf.fit(all_vals, all_ticker)
        prf = rf.predict_proba(y)
        self.prob["rf"] = prf

        print(self.prob)

        


