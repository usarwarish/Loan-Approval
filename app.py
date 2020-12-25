#import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template 
import pickle
import os
import pandas as pd

#app name
app = Flask(__name__)

#load the saved model
def load_model():
    return pickle.load(open('myModel.pkl','rb'))

#home page
@app.route('/')
def home():
    return render_template('index.html')

#predict the result and return it
@app.route('/predict', methods =['POST'])
def predict():

    labels =["Cannot be approved", " can be Approved"]

    features = [x for x in request.form.values()]

    '''
    'Loan_ID', 'Gender', 'Married', 'Dependents', 'Education',
       'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area',

    '''

    Loan_ID= str(features[0])
    

    Gender = str(features[1])
    if Gender.lower()=="female":
        g=np.array([1,0])
    else:
        g=np.array([0,1])


    Married = str(features[2])
    if Married.lower()=="no":
        marr=np.array([1,0])
    else:
        marr=np.array([0,1])

    d0,d1,d2,d3=0,0,0,0
    Dependents = str(features[3])
    if Dependents=="0":
        d0=1
    elif Dependents=="1":
        d1=1
    elif Dependents == "2":
        d2 =1
    else:
        d3=1
    depend =np.array([d3,d0,d1,d2])

    Education = str(features[4])
    if Education.lower() == "graduate":
        edu = np.array([1,0])
    else:
        edu = np.array([0,1])

    Self_Employed = str(features[5])
    if Self_Employed.lower()=="yes":
        se =np.array([0,1])
    else :
        se= np.array([1,0])
    
    ApplicantIncome = str(features[6])
    aic = float(ApplicantIncome)
    print(type(aic))
    CoapplicantIncome = str(features[7])
    coic = float(CoapplicantIncome)

    LoanAmount = str(features[8])
    loa = float(LoanAmount)

    Loan_Amount_Term = str(features[9])
    lot = float(Loan_Amount_Term)

    Credit_History = str(features[10])
    ch = float(Credit_History)

    Property_Area = str(features[11])
    if Property_Area.lower()=="urban":
        par =np.array([0,0,1])
    elif Property_Area.lower()=="semiurban":
        par = np.array([0,1,0])
    else:
        par =np.array([1,0,0])

    final=np.array([aic,coic,loa,lot,ch])
    values= np.concatenate( (final, g,marr, depend, edu,se,par), axis=0)
    values = values.reshape(1,-1)
    print(values)

    model = load_model()
    prediction = model.predict(values)

    result = labels[prediction[0]]


    return render_template('index.html', output ='Your Loan {}'.format(result))

if __name__ == "__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(port=port, debug =True, use_reloader = False)
    #app.run(debug=True) for local