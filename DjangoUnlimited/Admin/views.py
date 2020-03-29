from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required 

# Create your views here.

from .forms import InitialAdminForm, AdminForm, AddIndustryForm
from Accounts.views import isValidated
from .models import Admin
from .forms import EditAdminProfileForm
from Student.forms import EditStudentProfileForm

# Create your views here.

@staff_member_required 
def create_admin(request):
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
                    messages.info(request,'ERROR: Password must be 8 characters or more, and must have at least 1 uppercase, lowercase, numeric and special character.')
                    return redirect("admin_register")
        else:
            messages.info(request, user_form.errors)
            return redirect("admin_register")
    else:
        user_form = InitialAdminForm()
        admin_form = AdminForm()
        args = {'admin_form': admin_form, 'user_form': user_form}
        return render(request, 'admin/admin_registration.html', args)

@staff_member_required
def view_profile(request):
    user = request.user
    admin = Admin.objects.get(user_id=user.id)
    args = {'admin': admin, 'user': user}
    return render(request, 'admin/view_admin_profile.html', args)

@staff_member_required 
def edit_profile(request):
    admin = Admin.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = EditAdminProfileForm(request.POST, instance=request.user)
        admin_form = AdminForm(request.POST, request.FILES, instance=admin)

        if user_form.is_valid() and admin_form.is_valid():
            with transaction.atomic():
                user_form.save()
                admin_form.save()
                return render(request, 'admin/index.html')
        else:
            messages.info(request, admin_form.errors)
            messages.info(request, user_form.errors)
            return redirect("edit_admin_profile")
    else:
        user_form = EditAdminProfileForm(instance=request.user)
        admin_form = AdminForm(instance=admin)
        args = {'admin_form': admin_form, 'user_form': user_form}
        return render(request, 'admin/edit_admin_profile.html', args)
