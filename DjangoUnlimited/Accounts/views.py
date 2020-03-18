from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView

from Employer.models import Employer
from Student.forms import studentIDForm, InitialStudentForm
from Employer.forms import companyNameForm, initialEmployerForm, completeEmployerForm

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

def employer_signup(request):

    if request.method == 'POST':

        compNameForm = companyNameForm(request.POST)
        form = initialEmployerForm(request.POST)

        if compNameForm.is_valid and form.is_valid():

            if form.usernameExists():
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("employer_register")

            elif form.emailExists() == True:
                messages.info(request, 'Email already taken. Try a different one.')
                return redirect("employer_register")

            elif form.samePasswords() == False:
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("employer_register")

            elif form.emailDomainExists() == False:
                messages.info(request, 'Email domain does not exist. Try again.')
                return redirect("register")

            else:
                # if (isValidaam.cleaned_data.get('password1'))): # if password meets validation criteria
                    user = form.save()

                    employer = compNameForm.save(commit=False)
                    employer.user = user
                    employer.company_name = compNameForm.cleaned_data.get('companyName')
                    employer.save()

                    return redirect("log_in")

                # else:
                #     messages.info(request, 'ERROR: Password must be 8 characters or more, and must have atleast 1 uppercase, lowercase, numeric and special character.')   
                #     return redirect("employer_register")


        else:
            messages.info(request, form.errors)
            return redirect("employer_register")
    else:
        form = initialEmployerForm() 
        compNameForm = companyNameForm()
        return render(request, 'employer_registration.html', {'form': form, 'compNameForm': compNameForm})


def student_signup(request):

    if request.method == 'POST':

        studIDForm = studentIDForm(request.POST)
        form = initialStudentForm(request.POST)

        if studIDForm.is_valid and form.is_valid():

            if form.usernameExists() == True:
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("register")

            elif form.emailExists() == True:
                messages.info(request, 'Email already taken. Try a different one.')
                return redirect("register")

            if form.emailDomainExists() == False:
                messages.info(request, 'Email domain does not exist. Try again.')
                return redirect("register")

            elif form.samePasswords() == False:
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("register")

            else:
            #     if (isValidated(form.cleaned_data.get('password1'))): # if password meets validation criteria
                    user = form.save()

                    # student = Student()
                    # student.user = user
                    # student.save()
                
                    student = studIDForm.save(commit=False)
                    student.user = user
                    student.student_id = studIDForm.cleaned_data.get('studentID')
                    student.save()

                    return redirect('log_in')
                    # return redirect('password_reset')

                # else:
                #     messages.info(request, 'ERROR: Password must be 8 characters or more, and must have atleast 1 uppercase, lowercase, numeric and special character.')   
                #     return redirect("register")

        else:
            messages.info(request, form.errors)
            return redirect("register")

    else:
        form = initialStudentForm() 
        return render(request, 'registration.html', {'form': form})


def login(request):

    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is None:
                messages.info(request, 'Credentials do not exist, please try a different username/password')
                return redirect("log_in")
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
