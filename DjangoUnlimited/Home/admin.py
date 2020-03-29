from django.contrib import admin
from .models import Industry, Skill, Job, JobType

class JobAdmin(admin.ModelAdmin):
    exclude = ('date_posted', 'status', 'date_closed')
    list_display = ('job_title', 'description', 'salary')

# Register your models here.
admin.site.register(Job, JobAdmin)
admin.site.register(JobType)
admin.site.register(Industry)
admin.site.register(Skill)