from django.shortcuts import render
from Employer.models import Employer

def index(request):
    return render(request, 'Index.html')
    # {'emp': request.user}
