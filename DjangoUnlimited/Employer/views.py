from django.shortcuts import render
#from .forms import EmployerForm

# Create your views here.

def edit_employer_profile(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        phone_number = request.POST['phone_number']
    else:
        return render(request, 'edit_employer_profile.html')