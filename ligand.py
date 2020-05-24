import os
from werkzeug.utils import secure_filename

class Ligand:
     number = 0

     @staticmethod
     def save(ligand, instance_path):
        num = Ligand.number
        ligand.save(os.path.join(instance_path, 'ligand', secure_filename(str(Ligand.number) + '.pdbqt')))
        Ligand.number += 1
        return '/ligand/' + str(num) + '.pdbqt'
