from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobPost, JobDescription


class RegisterForm(UserCreationForm):
  MYCHOICES = [
     ('Student', 'I am looking for internship'),
     ('Employer', 'I am looking for interns'),
  ]

  email = forms.EmailField(required=True)  
  first_name = forms.CharField(required=True)
  last_name = forms.CharField(required=True)  
  status = forms.ChoiceField(
     choices = MYCHOICES,
     initial = 'Student',
     widget = forms.Select)      

  class Meta:                         # the RegisterForm is going to be saved into the user's database
    model = User
    fields = ["username", 
              "email",               
              "first_name",
              "last_name",     
              "status",       
            ] # Layout where the fields need to be, order. Fields are already defined in UserCreationForm, except "ëmail". Feel free to add more here like "gender" 


class JobPostForm(ModelForm):   
  degree = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'e.g.: Bachelor of Science in Computer Science'})
  )
  school = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'University where you have earned your degree'})
  )
  biography = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'Interests, hobbies, preferences, ...'})
  )

  class Meta:
    model = JobPost
    fields = ["username",
              "applicant_contact_number",
              "email",
              "first_name",
              "last_name",
              "degree",
              "school",
              "GPA",
              "curricular_skills",
              "noncurricular_skills",
              "biography",
              "file_upload_CV",
            ]
      
  def __init__(self, *args, **kwargs):
    super(JobPostForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget = forms.HiddenInput() 
    self.fields['email'].widget = forms.HiddenInput() 
    self.fields['first_name'].widget = forms.HiddenInput() 
    self.fields['last_name'].widget = forms.HiddenInput() 


class JobDescriptionForm(ModelForm):
  
  location = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'Area of deployment'})   
  )
  title = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'Title of the vacancy/position'})
  )
  term = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'e.g.: Contractual, Part-time, Full-time, ...'})
  )
  category = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'Information Technology, Business, Engineering, ...'})
  )
  department = forms.CharField(
    widget=TextInput(attrs={'placeholder': 'e.g.: ERP Office, MIS Department, Career Center, ...'})
  )

  class Meta:
    model = JobDescription
    fields = ["username",
              "jd_id",
              "contact_number",
              "contact_person",
              "email",
              "company_name",
              "location",
              "title",
              "term",
              "category",
              "department",
              "qualifications",
              "job_requirements",
              "file_upload",
            ]    
    
  def __init__(self, *args, **kwargs):
    super(JobDescriptionForm, self).__init__(*args, **kwargs)
    self.fields['username'].widget = forms.HiddenInput() 
    self.fields['email'].widget = forms.HiddenInput() 
    self.fields['jd_id'].widget = forms.HiddenInput()
   