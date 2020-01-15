# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 20:13:16 2019

@author: gurka
"""
#API requirements
from flask import Flask, jsonify, request, json
import pickle
from flask import render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.

# general and data handling
import numpy as np
import os
from collections import Counter

# Required RDKit modules
import rdkit as rd
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit import RDConfig
from rdkit.Chem import PandasTools
from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdFingerprintGenerator
from rdkit import DataStructs
from rdkit.Chem import AllChem as Chem



# Load model
model = pickle.load(open('model.pkl', 'rb'))


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])

def predict():

    smile = [str(x) for x in request.form.values()]

    mol_gen = Chem.MolFromSmiles(smile[0])
    fp_array = [Chem.RDKFingerprint(mol_gen)]
    fp_final = []

    #convert fingerprint to sparse 2048kb array
    for fp in fp_array:
        arr = np.zeros((1,))
        DataStructs.ConvertToNumpyArray(fp, arr)
        fp_final.append(arr)

    #predictions
    result = model.predict([fp_final[0]])
    output = []

    if result == '0':
        output.append("This molecule is likely not an environmental carcinogen!")
    elif result == '1':
        output.append("This molecule has properties similar to known environmental carcinogens")

    #send results to browser
    #output = {'results': print(result[0])}
    #output = if result == 0
    #output_dict = {"This molecule is likely not an environmental carcinogen!": 0, "This molecule has properties similar to known environmental carcinogens": 1}

    #output = { ("This molecule is likely not an environmental carcinogen!" if result == 0 else "This molecule has properties similar to known environmental carcinogens"):("this molecule has properties similar to known environmental carcinogens" if result != 0
     #     else "This molecule is likely not an environmental carcinogen!") for key, value in output_dict.items() }


    #return data
    return render_template('index.html', prediction_text=output[0])

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
