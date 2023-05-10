from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Applicant, Job, JobApplication, Employer

class SignupForm(UserCreationForm):
    
    ACCOUNT_TYPE_CHOICES = [('applicant', 'Job Seeker'), ('employer', 'Employer')]

    password1=forms.CharField(label='Password', widget = forms.PasswordInput
    (attrs={'class':'form-control'}))

    password2=forms.CharField(label='Confirm Password(again)',
    widget=forms.PasswordInput(attrs={'class':'form-control'}))

    # email=forms.EmailField(required=True, widget = forms.EmailInput
    # (attrs={'class':'form-control'}))

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    class Meta:
        model= User
        #model._meta.get_field('email')._unique = True
        fields= ['email','password1','password2', 'account_type']
        labels= {'email':'Email',
                 'password1' : 'Enter Password',
                 'password2' : 're-enter Password',
                 'account_type': 'Account Type'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = (self.cleaned_data.get('account_type') == 'employer')
        if commit:
            user.save()
            if user.is_employer:
                Employer.objects.create(user=user)
            else:
                Applicant.objects.create(user=user)
        return user
   


class LoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs=
    {'autofocus':True, 'class': 'form-control'}))

    password = forms.CharField(label= ("Password"), strip=False,
    widget=forms.PasswordInput(attrs  =
    {'autocomplete':'current-password', 'class': 'form-control'}))


# class ApplicantProfileForm(forms.ModelForm):
#     class Meta:
#         model = Applicant
#         fields = ['name', 'phone', 'image', 'gender', 'address']
#         widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 
#         'phone':forms.NumberInput(attrs={'class': 'form-control'}), 
#         'image' : forms.ImageField(attrs={'class': 'form-control'}),
#         'gender': forms.Select(attrs={'class': 'form-control'}),
#         'address': forms.TextInput(attrs={'class': 'form-control'})
#         }

class PostJobForm(forms.ModelForm):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
    ]

    LOCATION_CHOICES = [
        ('Bangalore', 'Bangalore'),
        ('Chennai', 'Chennai'),
        ('Delhi', 'Delhi'),
        ('Hyderabad', 'Hyderabad'),
        ('Kolkata', 'Kolkata'),
        ('Mumbai', 'Mumbai'),
        ('Pune', 'Pune'),
    ]

    STATUS_CHOICES = [
        (True, 'Published'),
        (False, 'Disabled'),
    ]

    job_title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_type = forms.ChoiceField(choices=Job.JOB_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    #job_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.ChoiceField(choices=LOCATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    featured_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    company_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #company_description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    logo = forms.ImageField(label='Company Logo' , required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    last_date_of_application = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    salary_min = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    salary_max = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    experience_min = forms.IntegerField(label='Minimum Experience (years)', required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    experience_max = forms.IntegerField(label='Maximum Experience (years) set 0 for freshers' ,required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Job
        fields = [

            'job_title',
            'location',
            'job_type',
            'salary_min',
            'salary_max',
            'experience_min',
            'experience_max',
            'job_description',
            'last_date_of_application',
            'featured_image',
            'company_name',
            'logo',   
            'company_description',
            'email',
            
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['featured_image'].label = 'Featured Image (Leave blank if none)'
        self.fields['logo'].label = 'Company Logo (Leave blank if none)'

        # set image name value for existing job post
        if self.instance.featured_image:
            self.fields['featured_image'].initial = self.instance.featured_image.name
            self.fields['featured_image'].widget.attrs['value'] = self.instance.featured_image.name
            self.fields['featured_image'].widget.attrs['readonly'] = True

        if self.instance.logo:
            self.fields['logo'].initial = self.instance.logo.name
            self.fields['logo'].widget.attrs['value'] = self.instance.logo.name
            self.fields['logo'].widget.attrs['readonly'] = True



class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'gender', 'dob', 'email', 'phone_no', 'address', 'resume', 'cover_letter',  'linkedin', 'portfolio_links']
        widgets = {
            # 'applicant': forms.HiddenInput(),
            # 'job': forms.HiddenInput(),

            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),

            'gender': forms.Select(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control'}),

            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_links': forms.URLInput(attrs={'class': 'form-control'}),
            
            #'passport_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            
            
        }