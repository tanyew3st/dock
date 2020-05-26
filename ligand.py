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
      pdf = FPDF()
      pdf.add_page()
      pdf.set_font('Times','',10.0) 
      


      objects = affinity.keys()
      y_pos = np.arange(len(objects))
      value = []
      for i in affinity:
      value.append(affinity[i])

      plt.bar(y_pos, value, align='center', alpha=0.5)
      plt.xticks(y_pos, objects)
      plt.ylabel('Values')
      plt.title('Affinity Scores')

      plt.savefig('image.png')
      

      return ""


