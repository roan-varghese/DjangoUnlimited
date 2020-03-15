from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from Student.models import Student
from Employer.models import Employer
from Student.forms import initialStudentForm
from Employer.forms import companyNameForm, initialEmployerForm, completeEmployerForm

def isValidated(passwd):
    special_symbols = {'$', '@', '%', '&', '?', '.', '!', '#', '*', ' '}
    status = True

    if (len(passwd) > 8):
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
    # <--------------- USING DJANGO FORMS ------------------>
    if request.method == 'POST':

        compNameForm = companyNameForm(request.POST)
        form = initialEmployerForm(request.POST)

        if compNameForm.is_valid and form.is_valid():

            if form.usernameExists() == True:
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("employer_register")

            elif form.samePasswords() == False:
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("employer_register")

            else:
                user = form.save()
                employer = compNameForm.save(commit=False)
                employer.user = user
                employer.company_name = compNameForm.cleaned_data.get('companyName')
                employer.save()

                # username = form.cleaned_data.get('email')
                # raw_password = form.cleaned_data.get('password1')
                # user = auth.authenticate(username=username, password=raw_password)
                # auth.login(request, user)
                # return redirect('/')
                return redirect("login")

        else:
            messages.info(request, form.errors)
            return redirect("employer_register")

    else:
        form = initialEmployerForm() 
        compNameForm = companyNameForm()
        return render(request, 'employer_registration.html', {'form': form, 'compNameForm': compNameForm})


    # <--------------- USING HTML FORMS ------------------>
    # if request.method == 'POST':

        # companyName = request.POST['companyName']
        # email = request.POST['email']
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        
        # if password1==password2:
        #     if User.objects.filter(username=email).exists():
        #         messages.info(request, 'Username already taken. Try a different one.')
        #         return redirect("employer_register")

        #     else:
        #         # if (isValidated(password1)):
        #             user = User.objects.create_user(username=email, password=password1, email=email)
        #             employer = Employer()
        #             employer.user = user
        #             employer.company_name = companyName
        #             user.save()

        #             return redirect('login')

        #         # else:
        #         #     messages.info(request, 'ERROR: Password must be 8 characters or more, and must have atleast 1 uppercase, lowercase, numeric and special character.')   
        #         #     return redirect("employer_register")
    #     else:
    #         messages.info(request, 'Passwords not matching. Try again.')
    #         return redirect("employer_register")

    # else:
    #     return render(request, 'employer_registration.html')

def student_signup(request):
    # <--------------- USING DJANGO FORMS ------------------>
    if request.method == 'POST':

        form = initialStudentForm(request.POST)

        if form.is_valid():

            if form.usernameExists() == True:
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("register")

            elif form.samePasswords() == False:
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("register")

            else:
                user = form.save()
                # username = form.cleaned_data.get('email')
                # raw_password = form.cleaned_data.get('password1')
                # user = auth.authenticate(username=username, password=raw_password)
                # auth.login(request, user)
                # return redirect('/')
                return redirect("login")

        else:
            messages.info(request, form.errors)
            return redirect("register")

    else:
        form = initialStudentForm() 
        return render(request, 'registration.html', {'form': form})




    # <--------------- USING HTML FORMS ------------------>
    # if request.method == 'POST':
    #     studentID = request.POST['studentID']
    #     email = request.POST['email']
    #     password1 = request.POST['password1']
    #     password2 = request.POST['password2']
        
    #     if password1==password2:
    #         if User.objects.filter(username=studentID).exists():
    #             messages.info(request, 'Username already taken. Try a different one')
    #             return redirect("register")

    #         elif User.objects.filter(email=email).exists():
    #             messages.info(request, 'Email already used. Try a different one')
    #             return redirect("register")

    #         else:
    #             # if (isValidated(password1)):
    #                 user = User.objects.create_user(username=studentID, password=password1, email=email)
    #                 user.save()

    #                 return redirect('login')

    #             # else:
    #             #     messages.info(request, 'ERROR: Password must be 8 characters or more, and must have atleast 1 uppercase, lowercase, numeric and special character.')   
    #             #     return redirect("register")
    #     else:
    #         messages.info(request, 'Password not matching. Try again.')
    #         return redirect("register")

    # else:
    #     return render(request, 'Registration.html')

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
