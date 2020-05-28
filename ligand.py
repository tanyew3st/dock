import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from fpdf import FPDF

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
        print(protein)
        print(active)
        # active either 'active' or 'decoy'
        # protein will be 'akt1' or 'lck'
        return ""

        # return dictionary - structure: affinity for the first element in xslx

