from django import forms
from Home.models import Job, Skill, JobType, Industry

class CreateJobForm(forms.ModelForm):
    job_title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
         attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    description = forms.CharField(label = 'Job Description', max_length=100, required=True, widget=forms.Textarea(
         attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    duration = forms.DurationField()
    location = forms.CharField(max_length = 100, required = True)
    job_type_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=JobType.objects.all(),
        #required = True
        )
    salary = forms.FloatField()
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.all(),
        #required = True
        )

    industry_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset = Industry.objects.all(),
        #required = True,
        )

    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'status', 'date_closed']


class EditJobForm(forms.ModelForm):
    job_title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
         attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    description = forms.CharField(label = 'Job Description', max_length=100, required=True, widget=forms.Textarea(
         attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    job_status = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Deleted', 'Deleted')
    ]
    status = forms.ChoiceField(choices=job_status, widget=forms.Select(attrs={'class': 'custom-select'}))
    duration = forms.DurationField()
    location = forms.CharField(max_length = 100, required = True)
    job_type_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=JobType.objects.all(),
        #required = True
        )
    salary = forms.FloatField()
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.all(),
        #required = True
        )

    industry_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset = Industry.objects.all(),
        #required = True,
        )

    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'date_closed']