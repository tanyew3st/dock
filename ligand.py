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
     def makePDF(affinity, ml):
         pdf.add_page()
         pdf.set_font('Times','',10.0) 
         

         return ""


