from django import forms
from Home.models import Job, Skill, JobType, Industry
from Student.models import Student

from DjangoUnlimited import settings


class CreateJobForm(forms.ModelForm):
    job_title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    description = forms.CharField(label='Job Description', max_length=100, required=True, widget=forms.Textarea(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    duration = forms.IntegerField(label='Duration (in months)')
    location = forms.CharField(max_length=100, required=True)
    job_type_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=JobType.objects.all(),
        # required = True
    )
    salary = forms.FloatField()
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.all(),
        # required = True
    )

    industry_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=Industry.objects.all(),
        # required = True,
    )

    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'status', 'date_closed']


class EditJobForm(forms.ModelForm):
    job_title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control-text', 'style': 'resize:none;'}))
    description = forms.CharField(label='Job Description', max_length=100, required=True, widget=forms.Textarea(
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
        # required = True
    )
    salary = forms.FloatField()
    skills = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Skill.objects.all(),
        # required = True
    )

    industry_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=Industry.objects.all(),
        # required = True,
    )

    class Meta:
        model = Job
        exclude = ['posted_by', 'date_posted', 'date_closed']


class FilterJobForm(forms.ModelForm):
    min_duration = forms.IntegerField(required=False)
    max_duration = forms.IntegerField(required=False)
    location = forms.CharField(max_length=100, required=False)
    job_type_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=JobType.objects.all(),
        required=False
    )
    min_salary = forms.FloatField(required=False)
    max_salary = forms.FloatField(required=False)

    industry_id = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'custom-select'}),
        queryset=Industry.objects.all(),
        required=False
    )

    class Meta:
        model = Job
        fields = ['min_duration', 'max_duration', 'location', 'job_type_id', 'min_salary', 'max_salary',
                  'industry_id']

    def __init__(self, *args, **kwargs):
        super(FilterJobForm, self).__init__(*args, **kwargs)
        self.fields['job_type_id'].required = False
        self.fields['industry_id'].required = False


class FilterStudentForm(forms.Form):
    alumni_status = forms.BooleanField(required=False, label='Alumni Student',
                                       widget=forms.CheckboxInput(attrs={'onClick': 'disable_fields(this.checked)'}))

    min_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
                                               label='Minimum Graduation Date',
                                               widget=forms.DateInput(attrs={
                                                   'class': 'datepicker form-control-text',
                                                   'placeholder': 'YYYY-MM-DD',
                                                   'autocomplete': 'off'
                                               }))
    max_graduation_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False,
                                          label='Maximum Graduation Date',
                                          widget=forms.DateInput(attrs={
                                              'class': 'datepicker form-control-text',
                                              'placeholder': 'YYYY-MM-DD',
                                              'autocomplete': 'off'
                                          }))

    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)

    class Meta:
        model = Student
        fields = ['alumni_status', 'skills']
