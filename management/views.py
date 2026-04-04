import os
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
import pandas as pd

from Employess.models import employeeRegistrationModel

def managementHome(request):
    return render(request, 'Management/managementhome.html')

# Create your views here.
def managementLoginCheck(request):
    if request.method=="POST":
       loginid=request.POST['loginid']
       pswd=request.POST['pswd']
       if loginid=='admin' and pswd=='admin':
           
           return render(request,'Management/managementhome.html')
       else:
            messages.error(request, 'Please enter details carefully')

            return render(request,'ManagementLogin.html')

def employeeDetails(request):
    ud=employeeRegistrationModel.objects.all()
    print(ud)
    return render(request,'Management/employeeDetais.html',context={'ud':ud})

def datasetdetails(request):
    path = os.path.join(settings.MEDIA_ROOT, 'insurance fraud claims.csv')
    data = pd.read_csv(path, nrows=100).to_html()
    return render(request, 'Management/datasetreview.html', context={'data': data})


def updateEmployeeStatus(request):
    loginid=request.GET['loginid']
    usu=employeeRegistrationModel.objects.get(loginid=loginid)
    if usu.status=='waiting':
        usu.status='Activated'
        usu.save()
        ud=employeeRegistrationModel.objects.all()
        print(ud)
        return render(request,'Management/employeeDetais.html',context={'ud':ud})


    


