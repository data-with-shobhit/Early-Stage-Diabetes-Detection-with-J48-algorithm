import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
import random
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid
from django.conf import settings
############################################################################################################
#                                       User Authentication Function                                       #
############################################################################################################
def name_valid(name):
    if name.isalpha() and len(name) > 2:
        return True
    else:
        return False

def password_valid(pass1):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
	
	# compiling regex
    pat = re.compile(reg)
	
	# searching regex				
    mat = re.search(pat, pass1)
	
	# validating conditions
    if mat:
        return True
    else:
        return False

def password_check(password1, password2):
    if password1 == password2:
        return True
    else : 
        return False

def contact_valid(number):
    Pattern = re.fullmatch("[6-9][0-9]{9}",number)
    if Pattern != None:
        return True
    else:
        return False

def authentication(first_name, last_name, pass1, pass2):
    if name_valid(first_name) == False:
        return "Invalid First Name"           
    elif name_valid(last_name) == False:
            return "Invalid Last Name"
    elif password_valid(pass1) == False:
        return "Password Should be in Prpper Format. (eg. Password@1234)"
    elif password_check(pass1, pass2) == False:
        return "Password Not Matched"
    else:
        return "success"
############################################################################################################
#                                         Input Values Validation                                          #
############################################################################################################
def age_valid(age):
    if int(age) <= 120 and int(age) >= 0:
        return True
    else:
        return False

def pregnancies_valid(pregnancies):
    if int(pregnancies) >= 0:
        return True
    else:
        return False

def glucose_valid(glucose):
    if int(glucose) >= 0 and int(glucose) <= 200:
        return True
    else:
        return False

def blood_pressure_valid(blood_pressure):
    if int(blood_pressure) >= 0 and int(blood_pressure) <= 270:
        return True
    else:
        return False

def skin_thikness_valid(skin_thikness):
    if int(skin_thikness) >= 1 and int(skin_thikness) <= 50:
        return True
    else:
        return False

def insulin_valid(insulin):
    if int(insulin) >= 0 and int(insulin) <= 1153:
        return True
    else:
        return False

def bmi_valid(bmi):
    bmi = float(bmi)
    if bmi >= 0 and bmi <= 70:
        return True
    else:
        return False

def dpf_valid(dpf):
    dpf = float(dpf)
    if dpf >= 0 and dpf <= 3:
        return True
    else:
        return False

def input_validation(p_fname, p_lname, contact_no, age, pregnancies, glucose, blood_pressure, skin_thikness, insulin, bmi, dpf):
    if name_valid(p_fname) == False:
        return "Invalid First Name"           
    elif name_valid(p_lname) == False:
        return "Invalid Last Name"
    elif contact_valid(contact_no) == False:
        return "Invalid Contact Number"
    elif age_valid(age) == False:
        return "Invalid Age Details"
    elif pregnancies_valid(pregnancies) == False:
        return "Invalid Pregnancies Details"
    elif glucose_valid(glucose) == False:
        return "Invalid Glucose"
    elif blood_pressure_valid(blood_pressure) == False:
        return "Invalid Blood Pressure Details"
    elif skin_thikness_valid(skin_thikness) == False:
        return "Invalid Skin Thickness Details"
    elif insulin_valid(insulin) == False:
        return "Invalid Insulin Details"
    elif bmi_valid(bmi) == False:
        return "Invalid BMI Details"
    elif dpf_valid(dpf) == False:
        return "Invalid Diabetes Pedigree Function Details"
    else:
        return "success"

############################################################################################################
#                            Diabetes Prdiction Function using J48 Algorithm                               #
############################################################################################################
def diabetes_prediction(pregnancies,glucose,blood_pressure, skin_thikness, insulin, bmi, dpf, age):
    diabetes_dataset = pd.read_csv('dataset/diabetes.csv')
    diabetes_dataset['Outcome'].value_counts()
    diabetes_dataset.groupby('Outcome').mean()
    X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
    Y = diabetes_dataset['Outcome']

    scaler = StandardScaler()
    scaler.fit(X)
    standardized_data = scaler.transform(X)

    X = standardized_data
    Y = diabetes_dataset['Outcome']

    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify=Y, random_state=2)

    classifier = svm.SVC(kernel='linear')

    classifier.fit(X_train, Y_train)

    input_data = (pregnancies,glucose,blood_pressure, skin_thikness, insulin, bmi, dpf, age)

    input_data_as_numpy_array = np.asarray(input_data)

    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    std_data = scaler.transform(input_data_reshaped)

    prediction = classifier.predict(std_data)
    return prediction


############################################################################################################
#                                                Print Page                                                #
############################################################################################################

def html_to_pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    file_name = uuid.uuid4()

    try:
        with open(f'Patient_Reports/{file_name}.pdf', 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
    except Exception as e: 
        print(e)
    if pdf.err:
        return "", False
    return file_name, True

def identify_precautions(pred):
    if pred == 0:
        return "Report Normal. But you should Take Care of yourself."
    else:
        precautions = ["Monitor blood sugar levels regularly,"
                    "Follow a healthy diet,"
                    "Exercise regularly",
                    "Maintain a healthy weight",
                    "Avoid smoking",
                    "Manage stress.",
                    "Attend regular check-ups",
                    "Keep your feet clean and dry",
                    "Wear comfortable and well-fitted shoes",
                    "Practice good oral hygiene",
                    "Get vaccinated against flu and pneumonia",
                    "Be careful with alcohol consumption",
                    "Carry a source of fast-acting glucose"]
        precautions_list = random.sample(precautions,5)
        precautions_list = ", ".join(precautions_list)
        return precautions_list