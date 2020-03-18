from django.contrib import admin
from .models import Student, StudentSkill, StudentJobApplication

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentSkill)
admin.site.register(StudentJobApplication)