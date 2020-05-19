import pandas as pd

class MachineLearning:
    affinity = None

    def __init__(self, affinity):
        self.affinity = affinity

    # input is the location of the folder of the pdbqt files
    # output is where it will be printed to
    # boolean active to add ticker 1 or 0 to the excel spreadsheet
    def createDirectory(inputdir, outputdir, active):

        collumns = []
        for i in inputdir:
            collumns.append(i)

        beginning = True
        maximum = 0
        for i in inputdir:
            dictionary = {}
            opened = open(i).readlines()
            
            for items in opened:
                num = ''
                for j in items.split()[1].split('_')[2]:
                    if j != '/':
                        num += j
                    else:
                        break
                if int(num) > maximum:
                    maximum = num
                dictionary[int(num)] = float(items.split()[0])
            if beginning == True:
                df = pd.dataFrame(index=np.arange(maximum + 1), columns = collumns)

            for k in range(1, maximum + 1):
                df.set_value(k, i, dictionary[k])
            beginning = False

        # end product to create a new excel spreadsheet .xlsx in the output location
    