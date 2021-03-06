import json
import os
import shutil
from ast import literal_eval
import time
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
    return render_template('models.html', option=option, proteins=Setup.getProteinNames())

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

@app.route('/sample/<protein>/<active>')
def getSampleScores(protein, active):
    dict = Ligand.getSample(protein, active)
    return make_response(jsonify(dict))


@app.route('/run/ml/array', methods=['POST'])
def runModels():
    data = json.loads(request.data)
    ml = MachineLearning(data['affinity'])
    ml.getProbability(data['protein'], data['linear'])
    print(ml.sens_spec_dict)
    return make_response(jsonify(ml.sens_spec_dict))

@app.route('/dock', methods=['POST'])
def dock():
    time.sleep(1)
    return make_response(jsonify({"affinity": -7.5}))
    data = json.loads(request.data)
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
    affinity = Setup.dock(p1, str(app.instance_path) + str(data['ligand']))
    obj = {"affinity": affinity}
    return make_response(jsonify(obj))

@app.route('/ml/render/page', methods=['POST'])
def renderml():
    affinity = request.form['textarea']
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

    if request.files:
        file_obj = request.files
        for f in file_obj:
            ligand = request.files.get(f)

    word = Ligand.save(ligand, app.instance_path)
    return render_template("results.html", ligand=word, protein = protein)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/predictions', methods=['POST'])
def file(protein, pdbqt):
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            print (file.filename)
    return ""

@app.route('/pdf')
def pdf():
    ligand = {"EGFR": 1, "EGFE": 2}
    ml = {"Support Vector Machines": [0.5, 0.5], "KNN": [0.4, 0.6]}
    pdf = Ligand.makePDF(ligand, ml)
    return app.send_static_file(pdf)


# Main method
if __name__ == "__main__":
    if os.path.isdir(os.path.join(app.instance_path, 'ligand')):
        shutil.rmtree(os.path.join(app.instance_path, 'ligand'))
    os.makedirs(os.path.join(app.instance_path, 'ligand'))
    app.run()


