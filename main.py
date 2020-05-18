import ligand
import os;

# selected by the user upon initial interaction with the API
protein = "EGFR"

directory = None

proteins = []

def dock(protein):
    command = ""

if __name__ == "__main__":
    # command = "./vina"
    # os.system(command)

    # property = ligand.openFile("conf.txt")
    # ligand.readFile(property)
    #
    # print ligand.properties
    property = ligand.openFile("conf.txt")
    ligand.readFile(property)

    print(ligand.properties)

    # choose name
    #change 2

    for i in os.listdir("proteins"):
        print(i)
        directory = "proteins/" + i
        print(directory)

    for i in os.listdir(directory):
        print("Protein" + i)

        # directory for the conf.txt
        prtdir = directory + "/" + i + "/conf.txt"
        print(prtdir)
        # proteins.append(ligand(prtdir))

    for i in protein:
        dock(i)
