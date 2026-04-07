import os
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

from Employess.models import employeeRegistrationModel

def managementHome(request):
    return render(request, 'Management/managementhome.html')

# Create your views here.
def managementLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        if loginid == 'admin' and pswd == 'admin':
            return render(request, 'Management/managementhome.html')
        else:
            messages.error(request, 'Please enter details carefully')
            return render(request, 'managementLogin.html')
    return render(request, 'managementLogin.html')

def employeeDetails(request):
    ud=employeeRegistrationModel.objects.all()
    print(ud)
    return render(request,'Management/employeeDetais.html',context={'ud':ud})

def datasetdetails(request):
    # import pandas lazily to avoid heavy startup imports
    import pandas as pd

    path = os.path.join(settings.MEDIA_ROOT, 'insurance fraud claims.csv')
    data = pd.read_csv(path, nrows=100).to_html()
    return render(request, 'Management/datasetreview.html', context={'data': data})


def updateEmployeeStatus(request):
    # Safely get loginid and handle missing or invalid values
    loginid = request.GET.get('loginid')
    if not loginid:
        messages.error(request, 'Missing login id for activation')
        ud = employeeRegistrationModel.objects.all()
        return render(request, 'Management/employeeDetais.html', context={'ud': ud})

    try:
        usu = employeeRegistrationModel.objects.get(loginid=loginid)
    except employeeRegistrationModel.DoesNotExist:
        messages.error(request, 'Employee not found')
        ud = employeeRegistrationModel.objects.all()
        return render(request, 'Management/employeeDetais.html', context={'ud': ud})

    if usu.status == 'waiting':
        usu.status = 'Activated'
        usu.save()

    ud = employeeRegistrationModel.objects.all()
    return render(request, 'Management/employeeDetais.html', context={'ud': ud})


    


