from django.shortcuts import render

# Create your views here.
import os
from django.shortcuts import render
from Employess.models import employeeRegistrationModel
from django.contrib import messages
from django.db import IntegrityError

def employeehome(request):
    return render(request, 'Employess/employeeHome.html', {})

# Create your views here.
def employeeRegister(request):
    if request.method=='POST':
        name=request.POST['name']
        loginid=request.POST['loginid']
        pswd=request.POST['pswd']
        mobile=request.POST['mobile']
        email=request.POST['email']
        state=request.POST['state']
        location=request.POST['location']

        ur = employeeRegistrationModel(name=name, loginid=loginid, password=pswd, email=email, state=state, location=location, mobile=mobile)
        try:
            print('Data is Valid')
            ur.save()
            messages.success(request, 'You have been successfully registered')
            return render(request, 'employeeRegistrations.html')
        except IntegrityError as e:
            # Handle unique constraint violations gracefully
            err_msg = str(e)
            print('Registration IntegrityError:', err_msg)
            if 'mobile' in err_msg:
                messages.error(request, 'Registration failed: Mobile number already registered.')
            elif 'loginid' in err_msg:
                messages.error(request, 'Registration failed: Login ID already exists.')
            elif 'email' in err_msg:
                messages.error(request, 'Registration failed: Email already registered.')
            else:
                messages.error(request, 'Registration failed due to duplicate data.')
            return render(request, 'employeeRegistrations.html')
        except Exception as e:
            # Log the exception to server logs for debugging and show a friendly message
            print('Registration error:', str(e))
            messages.error(request, 'Registration failed. Please check input and try again.')
            return render(request, 'employeeRegistrations.html')
    else:
      
        return render(request, 'assets/employeeRegistrations.html')

def employeeLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = employeeRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "Activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'Employess/employeeHome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'employeeLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'employeeLogin.html', {})

from django.conf import settings

def dataset(request):
    # import pandas lazily to avoid heavy startup imports
    import pandas as pd

    path = os.path.join(settings.MEDIA_ROOT, 'insurance fraud claims.csv')
    df = pd.read_csv(path, nrows=100)
    df = df.to_html()
    return render(request, 'Employess/datasetreview.html', {'data': df})

def prediction(request):
    return render(request, 'Employess/dataprediction.html')


def Classification_result(request):
    # import heavy ML work lazily to avoid expensive startup imports
    from utility.data_procesing import main

    accuracy, precision, recall = main()
    return render(request, 'Employess/view_classification_result.html', context={'accuracy': accuracy, 'precision': precision, 'recall': recall})


def fruad_prediction(request):
    # import prediction helper lazily
    from utility.data_procesing import prediction_value

    msg = ''
    if request.method == 'POST':
        policy_number = int(request.POST['policy_number'])
        collision_type = request.POST.get('collision_type')
        incident_severity = request.POST.get('incident_severity')
        authorities_contacted = request.POST.get('authorities_contacted')
        total_claim_amount = int(request.POST.get('total_claim_amount'))
        injury_claim = int(request.POST.get('injury_claim'))
        property_claim = int(request.POST.get('property_claim'))
        vehicle_claim = int(request.POST.get('vehicle_claim'))

        input_data = {
            'policy_number': policy_number,
            'collision_type': collision_type,
            'incident_severity': incident_severity,
            'authorities_contacted': authorities_contacted,
            'total_claim_amount': total_claim_amount,
            'injury_claim': injury_claim,
            'property_claim': property_claim,
            'vehicle_claim': vehicle_claim,
        }

        result = prediction_value(input_data)
        # prediction_value may return an array; normalize to first element
        try:
            val = result[0]
        except Exception:
            val = result
        msg = 'fraud claim detected' if val == 'Y' else 'its a real claim'
    return render(request, 'Employess/dataprediction.html', {'result': msg})


