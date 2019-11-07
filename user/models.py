from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)

class Genetic_disorder(models.Model):

    GD = (
        ('Haemophilia', 'Haemophilia'),
        ('Thalassemia', 'Thalassemia'),
        ('Down Syndrome', 'Down Syndrome'),
        ('Cystic Fibrosis', 'Cystic Fibrosis'),
        ('Sickle Cell Anemia', 'Sickle Cell Anemia'),  
        ('Hemochromatosis', 'Hemochromatosis'),                  
    )
    
    name=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.name

class Allergy(models.Model):

    ALG = (
        ('Eggs', 'Eggs'),
        ('Milk Products', 'Milk Products'),
        ('Peanuts', 'Peanuts'),
        ('Treenuts', 'Treenuts'),
        ('Fish', 'Fish'),  
        ('Wheat', 'Wheat'),              
    )
    
    name=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.name

class Patient(models.Model):

    SEX = (
        ('F', 'Female'),
        ('M', 'Male'),        
    )
    
    BG = (
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('AB+', 'AB+'),
        ('O+', 'O+'),
        ('A-','A-'),
        ('B-', 'B-'),
        ('AB-', 'AB-'),
        ('O-', 'O-'),                   
    )
    First_Name=models.CharField(max_length=100)
    Last_Name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    RFID=models.CharField(max_length=100,null=True,)
    DOB=models.DateField()
    sex=models.CharField(max_length=1,choices=SEX,)
    allergy=models.ManyToManyField(Allergy)
    genetic_disorder=models.ManyToManyField(Genetic_disorder)
    blood_group=models.CharField(max_length=5,choices=BG,null=True,blank=True)

    class Meta:
        ordering = ['First_Name','Last_Name']

    def __str__(self):
        return '{0} {1}'.format(self.First_Name,self.Last_Name)


    def get_absolute_urls(self):
        return reverse('')

class Prescription(models.Model):

    MD = (
        ('Synthroid', 'Synthroid'),
        ('Crestor', 'Crestor'),
        ('Ventolin HFA', 'Ventolin HFA'),
        ('Nexium', 'Nexium'),
        ('Lyrica', 'Lyrica'),  
        ('Vyvanse', 'Vyvanse'), 
        ('Lantus Solostar', 'Lantus Solostar'), 
        ('Advair Diskus', 'Advair Diskus'),              
    )

    DIS = (

        ('Asthama', 'Asthama'), 
        ('Cancer', 'Cancer'),
        ('Cholera', 'Cholera'),
        ('Common cold', 'Common cold'),
        ('Diarrhoea', 'Diarrhoea'),
        ('Dengue', 'Dengue'),
        ('Malaria', 'Malaria'),  
        ('Typhoid', 'Typhoid'),

                    
    )
    title=models.CharField(max_length=100)        
    date=models.DateField(default=datetime.date.today)      
    prescription_text=models.TextField()
    doctor=models.ForeignKey('Doctor',on_delete=models.SET_NULL, null=True)
    medicine=models.CharField(max_length=15,choices=MD,null=True)
    disease=models.CharField(choices=DIS,null=True,max_length=20)
    checked=models.BooleanField(default=False)
    patient=models.ForeignKey('Patient',on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['checked','-date']
    def __str__(self):
        return '{0} {1}'.format(self.id,self.title)

    def get_absolute_urls(self):
        return f'patient/prescription/{self.id}'

class Pharmacist(models.Model):
    Name=models.CharField(max_length=100)
    License_no=models.CharField(max_length=10)
    finger=models.CharField(max_length=10,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class Doctor(models.Model):

    First_name=models.CharField(max_length=100)
    Last_name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    finger=models.CharField(max_length=10,null=True)
    DEG=(('mbbs','MBBS'),('md','MD'),('ms','MS'),('dnb','DNB'))
    Degree=models.CharField(max_length=4,choices=DEG)
    SPL=(('Dermatology','Dermatology'),('General Medicine','General Medicine'),('Pharmacology','Pharmacology'),
         ('Pathology','Pathology'),('Paediatrics','Paediatrics'),('ENT','ENT'),('Orthopedics','Orthopedics'),
         ('Neurology','Neurology'),('Cardiology','Cardiology'),('Genral Surgery','Genral Surgery'))
    Speciality=models.CharField(max_length=30,choices=SPL)
    Hospital=models.CharField(max_length=100)

    class Meta:
        ordering = ['First_name','Last_name']

    def __str__(self):
        return '{0} {1}'.format(self.First_name,self.Last_name)