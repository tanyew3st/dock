# class variables for each Protein that need to be changed
class Protein:
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

    def __repr__(self):
        return str(self.properties)
        # return str(self.x)

    def openFile(self, name):
        propertyUO = {}
        o = open(name)
        opened = o.readlines()
        for i in opened:
            if i != "\n":
                propertyUO[i.split()[0]] = i.split()[-1]
        return propertyUO

    def __init__(self, name, directory):
        self.x = name
        propertyUO = self.openFile(name)
        self.properties = propertyUO
        # self.readFile(propertyUO)
        self.properties["receptor"] = directory + self.properties["receptor"]


    # Take in a file object and return a new Protein object
    def readFile(self, propertyUO):
        for i in propertyUO:
            self.properties[i] = propertyUO[i]
