import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd

class Ligand:
    number = 0

    @staticmethod
    def save(ligand, instance_path):
        num = Ligand.number
        ligand.save(os.path.join(instance_path, 'ligand', secure_filename(str(Ligand.number) + '.pdbqt')))
        Ligand.number += 1
        return '/ligand/' + str(num) + '.pdbqt'

    @staticmethod
    def getSample(protein, active):
      # active either 'active' or 'decoy'
      # protein will be 'akt1' or 'lck'
      if active == "active":
         activeDf = pd.read_excel("proteins/" + protein + "/active.xlsx", index=False)
      else:
         activeDf = pd.read_excel("proteins/" + protein + "/decoy.xlsx", index=False)
      
      activeDf.drop("Unnamed: 0", axis=1, inplace=True)

      first = (activeDf.iloc[0])
      return (first.to_dict())



      # return dictionary - structure: affinity for the first element in xslx

