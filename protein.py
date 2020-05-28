# class variables for each Protein that need to be changed
import os


class Protein:
    structure = None

    properties = {
        "receptor": None,
        "center_x": None,
        "center_y": None,
        "center_z": None,
        "size_x": None,
        "size_y": None,
        "size_z": None,
        "exhaustiveness": None
    }

    @staticmethod
    def getStructures(name):
        structures = os.listdir('proteins/' + name + '/Structures')
        for i in range(0, len(structures) - 1):
            if structures[i].lower() == ".ds_store":
                structures.remove(structures[i])
        return structures

    def __repr__(self):
        # return str(self.structure)
        return str(self.properties)
        return str(self.structure)

    def openFile(self, name):
        propertyUO = {}
        o = open(name)
        opened = o.readlines()
        for i in opened:
            if i != "\n":
                propertyUO[i.split()[0]] = i.split()[-1]
        return propertyUO

    # configuration is the location of the .conf or .txt file
    def __init__(self, configuration):
        directory = configuration.rsplit('/', 1)[0] + "/"
        propertyUO = self.openFile(configuration)
        self.properties = propertyUO
        # self.readFile(propertyUO)
        self.properties["receptor"] = directory + self.properties["receptor"]


    # Take in a file object and return a new Protein object
    def readFile(self, propertyUO):
        for i in propertyUO:
            self.properties[i] = propertyUO[i]
