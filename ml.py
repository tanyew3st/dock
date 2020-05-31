import collections

import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier;
from sklearn.ensemble import RandomForestClassifier;
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import math

# class to provide Machine Learning and create a model
class MachineLearning:
    # results should contain prob object
    # and affinity object
    results = {}

    # affinity scores made in the constructor
    affinity = None

    # probability object that contains all the probabilities for the various models
    prob = {}

    actives = None
    decoys = None

    sens_spec_dict = {}

    # on init set the affinity array equal to the affinity scores provided by vina
    def __init__(self, testaffinity):
        self.affinity = collections.OrderedDict(sorted(testaffinity.items()))
        print(self.affinity)

    # input is the location of the folder of the pdbqt files
    # output is where it will be printed to
    # boolean active to add ticker 1 or 0 to the excel spreadsheet
    @staticmethod
    def createDirectory(inputdir, outputdir, active):
        columns = []
        for i in os.listdir(inputdir):
            if i.__contains__("GetTop"):
                j = i.find(".")
                columns.append(i[0:j])
        columns = sorted(columns)
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
                    df.at[k, i[0:i.find('.')]] = float(dictionary[k])
                else:
                    missingData.append([k, i[0:i.find('.')]])
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

    # create a dictionary maximizing sensitivity and specificity
    def addToDict(self, tpr, fpr, thresholds, auc):
        temp = {}

        # want the first tpr = sensitivity >= 0.9 (threshold)
        # want the first 1-fpr = specificity <= 0.1 (threshold)

        for i in range(0, len(tpr)):
            if tpr[i] >= 0.9:
                temp["sensitivity"] = thresholds[i]
                break
        for i in range(0, len(fpr)):
            if 1 - fpr[i] <= 0.1:
                temp["specificity"] = thresholds[i]
                break

        maxg = 0
        best_threshold = 0

        for t in range(0, len(thresholds)):
            gmean = math.sqrt(tpr[t] * (1-fpr[t]))
            if gmean > maxg:
                maxg = gmean
                best_threshold = thresholds[t]
        temp["g-mean"] = best_threshold
        temp["auc"] = auc

        print("THE MAX G Value is " + str(maxg) + " and the threshold for that is " + str(best_threshold))
        return temp

    def predict(self, probability, name):
        print(self.sens_spec_dict[name])
        for i in self.sens_spec_dict[name]:
            print(i)

    # gets the probability using various machine learning models and sets
    def getProbability(self, protein, linear):

        # reading the active files from the excel spreadsheet
        actives = pd.read_excel("proteins/" + protein + "/active.xlsx", index=False)
        actives.drop("Unnamed: 0", axis=1, inplace=True)
        active_ticker = np.ones(len(actives))
        print('ACTIVES')

        # reading the decoy files from the excel spreadsheet
        decoys = pd.read_excel("proteins/" + protein + "/decoy.xlsx", index=False)
        decoys.drop("Unnamed: 0", axis=1, inplace=True)
        decoy_ticker = np.zeros(len(decoys))
        print('DECOYS')

        # creating all the values
        all_vals = pd.concat([actives, decoys], ignore_index=True)

        if all_vals.isnull().values.any():
            print(pd.isnull(all_vals).any(1).nonzero()[0])
            exit(4)

        # assigning 0 or 1 if it is active (1) or decoy (0)
        all_ticker = np.concatenate([active_ticker, decoy_ticker])

        X_train, X_test, y_train, y_test = train_test_split(all_vals, all_ticker, test_size=0.2, random_state=50)
        logModel = LogisticRegression(solver='lbfgs')
        logModel.fit(X_train, y_train)
        y_predict_proba = logModel.predict_proba(X_test)[:,1]
        fpr, tpr, thresholds = roc_curve(y_test, y_predict_proba, pos_label=1)

        print("AUC: " + str(auc(fpr, tpr)))

        self.sens_spec_dict["Logistic Regression"] = self.addToDict(tpr, fpr, thresholds, auc(fpr, tpr))

        print(self.sens_spec_dict)

        y = pd.DataFrame(self.affinity, index=[0])

        prob = logModel.predict_proba(y)
        self.predict(prob[:,1], "Logistic Regression")
        self.sens_spec_dict["Logistic Regression"]["probability"] = prob[0][1]
        print(self.sens_spec_dict)

        # Logistic Regression
        # print("Doing Logistic Regression")
        # logModel = LogisticRegression(solver='lbfgs')
        # logModel.fit(all_vals, all_ticker)
        # plr2 = logModel.predict_proba(y)
        # plr = logModel.predict_proba(y)[:, 1]
        # print(plr)
        # if plr > best_threshold:
        #     print('active')
        # else:
        #     print('decoy')
        # self.prob["lr"] = plr[0][0:].tolist()

        # K Nearest Neighbor
        y_predict_proba = logModel.predict_proba(X_test)[:, 1]
        fpr, tpr, thresholds = roc_curve(y_test, y_predict_proba, pos_label=1)
        auc_roc = auc(fpr, tpr)
        print("AUC KNN: " + str(auc_roc))
        maxg = 0
        best_threshold = 0
        for t in range(0, len(thresholds) - 1):
            gmean = math.sqrt(tpr[t] * (1 - fpr[t]))
            if gmean > maxg:
                maxg = gmean
                best_threshold = thresholds[t]
        print("THE MAX G Value is " + str(maxg) + " and the threshold for that is " + str(best_threshold))

        if all_vals.isnull().values.any():
            print(pd.isnull(all_vals).any(1).nonzero()[0])
            exit(4)

        # K Nearest Neighbors
        print("Doing KNN")
        knn = KNeighborsClassifier(n_neighbors=100)
        knn.fit(all_vals, all_ticker)
        pknn = knn.predict_proba(y)
        plr = knn.predict_proba(y)[:, 1]

        knn.fit(X_train, y_train)
        y_predict_proba = knn.predict_proba(X_test)[:, 1]
        fpr, tpr, thresholds = roc_curve(y_test, y_predict_proba, pos_label=1)

        print("AUC: " + str(auc(fpr, tpr)))

        self.sens_spec_dict["K Nearest Neighbors"] = self.addToDict(tpr, fpr, thresholds, auc(fpr, tpr))

        prob = knn.predict_proba(y)
        self.predict(prob[:, 1], "K Nearest Neighbors")
        self.sens_spec_dict["K Nearest Neighbors"]["probability"] = prob[0][1]
        print(self.sens_spec_dict)

        if not linear:
            # Support Vector Machines
            print("Doing Support Vector Machines")
            svc = SVC(C=1, gamma=0.1, probability=True, kernel="linear")
            svc.fit(all_vals, all_ticker)
            psvc = svc.predict_proba(y)
            self.prob["svc"] = psvc[0][0:].tolist()

            # Random Forest
            print("Doing Random Forest Classifier")
            rf = RandomForestClassifier(n_estimators=750)
            rf.fit(all_vals, all_ticker)
            prf = rf.predict_proba(y)
            self.prob["rf"] = prf[0][0:].tolist()

        print(self.prob)

        


