from __future__ import print_function

import json
import os
import shutil
from ast import literal_eval

import flask
from flask import render_template, request, send_file, jsonify, make_response

from ligand import Ligand
from ml import MachineLearning
from protein import Protein
from setup import Setup
# Configurations for Flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/run/<option>')
def switcher(option):
    if option != 'docking':
        return render_template('models.html', option=option, proteins=Setup.getProteinNames())
    else:
        return render_template('models.html', option=option)

@app.route('/post/ligand')
def postLigand(ligand):
    word = Ligand.save(ligand, app.instance_path)
    return word

@app.route('/structures/get/<name>')
def getStructures(name):
    return make_response(jsonify(Protein.getStructures(name)))

@app.route('/hello', methods=['POST'])
def sayHello():
    obj = {"hello": 'hello world'}
    return make_response(jsonify(obj))

@app.route('/run/ml/array', methods=['POST'])
def runModels():
    print('running')
    print(json.loads(request.data))
    data = json.loads(request.data)
    ml = MachineLearning(data['affinity'])
    ml.getProbability(data['protein'])

    return make_response(jsonify(ml.prob))

@app.route('/dock', methods=['POST'])
def dock():
    data = json.loads(request.data)
    print(data)
    directory = "proteins/" + str(data['protein']) + "/Structures/" + str(data['structure'])
    p1 = None
    for el in os.listdir(directory):
        extension = None
        if el.__contains__('.txt') or el.__contains__('.conf'):
            extension = el
        # directory for the conf.txt
        prtdir = directory + "/" + str(extension)

        # if to get rid of .ds-store and other weird files
        if extension is not None:
            p1 = Protein(prtdir)
    affinity = Setup.dock(p1, str(app.instance_path) + str(data['ligand'].encode('utf-8')))
    obj = {"affinity": affinity}
    print(obj)
    return make_response(jsonify(obj))

@app.route('/ml/render/page', methods=['POST'])
def renderml():
    affinity = request.form['textarea']
    print(affinity)
    # affinity = eval(affinity)
    return render_template("results.html", option="ml", affinity=affinity)

@app.route('/results')
def resultspage():
    return render_template("results.html")

@app.route('/run/ml/results', methods=['POST'])
def run():
    ligand = None
    protein = request.form['protein']

    data = dict(request.form)
    print("Data" + str(data))

    if request.files:
        file_obj = request.files
        for f in file_obj:
            ligand = request.files.get(f)

    print(ligand)
    word = Ligand.save(ligand, app.instance_path)
    print("Word: " + word)
    return render_template("results.html", ligand=word, protein = protein)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    print(app.instance_path)
    return render_template('about.html')

@app.route('/predictions', methods=['POST'])
def file(protein, pdbqt):
    # print(protein)
    # print(pdbqt)
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            print (file.filename)
    return ""


# Main method
if __name__ == "__main__":
    shutil.rmtree(os.path.join(app.instance_path, 'ligand'))
    os.makedirs(os.path.join(app.instance_path, 'ligand'))
    app.run()


