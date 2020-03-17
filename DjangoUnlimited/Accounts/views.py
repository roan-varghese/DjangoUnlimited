from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView

from Employer.models import Employer
from Employer.forms import companyNameForm, InitialEmployerForm, EmployerForm

def isValidated(passwd):
    special_symbols = {'$', '@', '%', '&', '?', '.', '!', '#', '*', ' '}
    status = True

    if len(passwd) > 8:
        status = True

    if not any(char.isdigit() for char in passwd): 
        status = False
          
    if not any(char.isupper() for char in passwd): 
        status = False
          
    if not any(char.islower() for char in passwd): 
        status = False
          
    if not any(char in special_symbols for char in passwd): 
        status = False
        
    return status

def login(request):

    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is None:
                messages.info(request, 'Credentials do not exist, please try a different username/password')
                return redirect("login")
            else:
                auth.login(request, user)
                print('User logged in')
                return redirect("/")
    else:
        return render(request, 'Login.html')

def forgot_password(request):
    if request.method == 'POST':
        return redirect("/")
    else:
        return render(request, 'Forgot_Password.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

# def confirm_logout(request):
#     return render(request, 'logout.html')

# def cancel_logout(request):
#     return redirect("/")
