"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user.views import (prescription_detailview, prescription_listview, home_view, base_view, DoctorSignUpView, DoctorView,
                        PatientSignUpView, PharmacistSignUpView)
from user.views import (PatientDetailView, PrescriptionCreateView, patient_prescription_view ,PatientDetailUpdateView,
                        prescription_detail_view,testview,userhome,PatientView,mydoctorview,patient_prescription_view)


app_name = 'emed'
urlpatterns = [
    path('signup/doctor',DoctorSignUpView.as_view(),name='doctor signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/patient',PatientSignUpView.as_view(),name='patient signup'),
    path('signup/pharmacist',PharmacistSignUpView.as_view(),name='pharmacist signup'),
    path('', home_view, name='home'),
    path('base/', base_view, name='base'),
    path('patient/prescription/list',prescription_listview.as_view(),name='prescription'),
    path('patient/prescription/<int:pk>',prescription_detailview.as_view(),name='prescription detail'),
    path('doctor/',DoctorView,name='doctor detail'),
    path('patient/',PatientView,name='patient detail'),
    path('test',testview,name='test'),
    path('mydoctors/',mydoctorview,name='my doctors'),
    path('myprescriptions',patient_prescription_view, name='p list'),
    path('user',userhome,name='user home')

]

urlpatterns += [
    path('search/patient',PatientDetailView.as_view(),name='patient search'),
    path('patient/prescription',PrescriptionCreateView.as_view(),name='prescription create'),
    path('patient/list',patient_prescription_view,name='prescription patient'),
    path('patient/update',PatientDetailUpdateView.as_view(), name='patient update'),    
    path('pharma/prescription/<int:pk>',prescription_detail_view,name='pharma prescription'),
]