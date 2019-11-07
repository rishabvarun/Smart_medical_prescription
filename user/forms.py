from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import Patient,Pharmacist,Doctor,User,Prescription
from .models import Allergy,Genetic_disorder

class PatientModelForm(forms.ModelForm):

    genetic_disorder=forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=Genetic_disorder.GD,
        required=False
    )

    allergy=forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=Allergy.ALG,
        required=False
    )
    
    class Meta:
        model=Patient
        fields=['blood_group','genetic_disorder','allergy']


class PrescriptionModelForm(forms.ModelForm):
    class Meta:
        model=Prescription
        fields=['title','date','disease','medicine','prescription_text']
 
 
class DoctorSignUpForm(UserCreationForm):    

    First_name=forms.CharField(max_length=100,required=True)
    Last_name=forms.CharField(max_length=100,required=True)
    finger=forms.CharField(max_length=10,required=False)
    Degree=forms.CharField(widget=forms.Select(choices=Doctor.DEG))
    Speciality=forms.CharField(widget=forms.Select(choices=Doctor.SPL))
    Hospital=forms.CharField(max_length=100,required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_doctor = True
        user.save()
        doctor = Doctor.objects.create(user=user)
        doctor.First_name=self.cleaned_data.get('First_name')
        doctor.Last_name=self.cleaned_data.get('Last_name')
        doctor.Speciality=self.cleaned_data.get('Speciality')
        doctor.Degree=self.cleaned_data.get('Degree')
        doctor.Hospital=self.cleaned_data.get('Hospital')
        doctor.finger=self.cleaned_data.get('finger')
        doctor.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),                
                css_class='form-row'
            ),
            'password1',
            'password2',
            Row(
                Column('First_name', css_class='form-group col-md-6 mb-0'),
                Column('Last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'finger',
            Row(
                Column('Speciality', css_class='form-group col-md-6 mb-0'),
                Column('Degree', css_class='form-group col-md-4 mb-0'),
                Column('Hospital', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            
            Submit('submit', 'Sign in')
        )

class PatientSignUpForm(UserCreationForm):
    

    First_name=forms.CharField(max_length=100,required=True)
    Last_name=forms.CharField(max_length=100,required=True)
    RFID=forms.CharField(max_length=100,required=False)
    Date_of_birth=forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},format='%Y/%m/%d'))   
    sex=forms.CharField(widget=forms.Select(choices=Patient.SEX))
    
    class Meta(UserCreationForm.Meta):
        model = User
        
    @transaction.atomic
    def save(self,request=None):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user,DOB='2000-01-27')
        patient.First_Name=self.cleaned_data.get('First_name')
        patient.Last_Name=self.cleaned_data.get('Last_name')
        patient.DOB=self.cleaned_data.get('Date_of_birth')
        patient.RFID=self.cleaned_data.get('RFID')
        patient.sex=self.cleaned_data.get('sex')        
        patient.save()
        request.session['user id']=patient.id  
        
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),                
                css_class='form-row'
            ),            
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('First_name', css_class='form-group col-md-6 mb-0'),
                Column('Last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'RFID',            
            Row(
                Column('Date_of_birth', css_class='form-group col-md-6 mb-0'),
                Column('sex', css_class='form-group col-md-4 mb-0'),                
                css_class='form-row'
            ),
            
            Submit('submit', 'Sign in')
        )

class PharmacistSignUpForm(UserCreationForm):
    

    Name=forms.CharField(max_length=100,required=True)
    License_no=forms.CharField(max_length=100,required=True)
    finger=forms.CharField(max_length=10,required=False)
    
    
    class Meta(UserCreationForm.Meta):
        model = User
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_pharmacist = True
        user.save()
        pharma = Pharmacist.objects.create(user=user)
        pharma.Name=self.cleaned_data.get('Name')
        pharma.License_no=self.cleaned_data.get('License_no')  
        pharma.finger=self.cleaned_data.get('finger')    
        pharma.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),                
                css_class='form-row'
            ),
            'password1',
            'password2',
            'finger',
            Row(
                Column('Name', css_class='form-group col-md-6 mb-0'),
                Column('License_no', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
                       
            Submit('submit', 'Sign in')
        )