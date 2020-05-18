import os
import ligand
import os;

protein = "EGFR";

def main():
    # command = "./vina"
    # os.system(command)

    property = ligand.openFile("conf.txt")
    ligand.readFile(property)

    print ligand.properties

    # choose name
    #change 2



main()