# class variables for each ligand that need to be changed

properties = {
    "receptor":None,
    "ligand":None,
    "center_x":None,
    "center_y":None,
    "center_z":None,
    "size_x":None,
    "size_y":None,
    "size_z":None,
    "exhaustiveness":None
}




def __init__(self):
    print("something")


def openFile(name):
    propertyUO = {}
    o = open(name)
    opened = o.readlines()
    for i in opened:
        if i != "\n":
            propertyUO[i.split()[0]] = i.split()[-1]
    return propertyUO
# Take in a file object and return a new Ligand object
def readFile(propertyUO):
    for i in propertyUO:
        properties[i] = propertyUO[i]
