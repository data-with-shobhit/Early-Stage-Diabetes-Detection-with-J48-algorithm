from django.shortcuts import render, redirect
from django.contrib import messages
from app.auth import authentication, diabetes_prediction, input_validation, identify_precautions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from app.models import Patients_Details
from datetime import datetime


# Create your views here.
def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html")

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return HttpResponseRedirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, "log_in.html")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(fname, contact_no, ussername)
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
            # return HttpResponse("This is Home page")
    return render(request, "register.html")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'fname': request.user.first_name, 
        'lname': request.user.last_name, 
        'username' : request.user
    }
    if request.method == "POST":
        p_fname = request.POST['p_fname']
        p_lname = request.POST['p_lname']
        contact_no = request.POST['contact_no']
        age = request.POST['age']
        pregnancies = request.POST['pregnancies']
        glucose = request.POST['glucose']
        blood_pressure = request.POST['blood_pressure']
        skin_thikness = request.POST['skin_thikness']
        insulin = request.POST['insulin']
        bmi = request.POST['bmi']
        dpf = request.POST['dpf']
        verify_input = input_validation(p_fname,p_lname,contact_no,age,pregnancies,glucose,blood_pressure, skin_thikness, insulin, bmi, dpf)
        if verify_input == 'success':
            pred = diabetes_prediction(pregnancies,glucose,blood_pressure, skin_thikness, insulin, bmi, dpf, age)
            if pred == 0:
                prediction = "Diabetes Not Detected"
                messages.info(request, "Diabetes Not Detected")
            else:
                prediction = "Diabetes Detected"
                messages.info(request, "Diabetes Detected")
            precautions = identify_precautions(pred)
            patient = Patients_Details(p_fname = p_fname, p_lname = p_lname, contact_no = contact_no, age = age, pregnancies = pregnancies, glucose = glucose, blood_pressure = blood_pressure, skin_thikness = skin_thikness, insulin = insulin, bmi = bmi, dpf = dpf)
            patient.prediction = prediction
            patient.precautions = precautions
            patient.date = datetime.today()
            patient.save()
            return redirect("patient_report")
        else:
            messages.error(request, verify_input)
            return redirect("dashboard")
    # return HttpResponse("This is Home page")    
    return render(request, "dashboard.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def patient_report(request):
    patient_data = Patients_Details.objects.last()
    context = {
        'fname': request.user.first_name, 
        'lname': request.user.last_name, 
        'username' : request.user,
        'patient_data' : patient_data
    }
    if request.method == "POST":
        return redirect("pdf_template")
    return render(request, "patient_report.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def pdf_template(request):
    patient_data = Patients_Details.objects.last()
    context = {
        'patient_data' : patient_data
    }
    return render(request, "pdf_template.html", context)