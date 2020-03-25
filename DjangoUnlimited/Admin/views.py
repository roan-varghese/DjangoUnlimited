from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required 

# Create your views here.

from .forms import InitialAdminForm, AdminForm, AddIndustryForm
from Accounts.views import isValidated
from Admin.models import Admin

# Create your views here.

@staff_member_required 
def createAdmin(request):
    if request.method == 'POST':
        user_form = InitialAdminForm(request.POST)

        if user_form.is_valid():
            if user_form.usernameExists():
                messages.info(request, 'Username already taken. Try a different one.')
                return redirect("admin_register")

            elif user_form.emailExists():
                messages.info(request, 'Email already taken. Try a different one.')
                return redirect("admin_register")

            elif not user_form.samePasswords():
                messages.info(request, 'Passwords not matching. Try again.')
                return redirect("admin_register")

            elif not user_form.emailDomainExists():
                messages.info(request, 'Email domain does not exist. Try again.')
                return redirect("admin_register")

            else:
                if isValidated(user_form.cleaned_data.get('password1')):
                    admin_form = AdminForm(request.POST, request.FILES)

                    if admin_form.is_valid():
                        with transaction.atomic():
                            user = user_form.save()
                            admin = admin_form.save(commit=False)
                            admin.user = user
                            admin.save()
                            return redirect("/")
                    else:
                        messages.info(request, admin_form.errors)
                        return redirect("admin_register")
                else:
                    messages.info(request,'ERROR: Password must be 8 characters or more, and must have atleast 1 uppercase, lowercase, numeric and special character.')
                    return redirect("admin_register")
        else:
            messages.info(request, user_form.errors)
            return redirect("admin_register")
    else:
        user_form = InitialAdminForm()
        admin_form = AdminForm()
        args = {'admin_form': admin_form, 'user_form': user_form}
        return render(request, 'admin/admin_registration.html', args)