from __future__ import print_function

import flask
from flask import render_template, request
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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
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
    app.run()


