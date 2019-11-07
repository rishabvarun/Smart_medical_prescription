from django.shortcuts import render,render_to_response,redirect
from django.views import generic
from .models import Patient,Prescription,Pharmacist,Doctor,User,Allergy,Genetic_disorder
from django.shortcuts import get_object_or_404
from .forms import DoctorSignUpForm, PatientSignUpForm, PharmacistSignUpForm
from .forms import PrescriptionModelForm, PatientModelForm
from django.contrib.auth import login,logout,authenticate
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import doctor_required,patient_required,pharmacist_required
from django import forms
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.views import View
from .hardware import give3




def home_view(request):
    return render(request,'home.html',{})

def base_view(request):
    return render(request,'base.html',{})

def userhome(request):    
    
    
    # if (request.user.is_doctor or request.user.is_pharmacist) and request.session['key']==1:
    #     return HttpResponseRedirect('test')
    return render(request,'userhome.html',{})


def testview(request):
    
    if not request.user.is_patient:
        if request.user.is_doctor:
            doctor=Doctor.objects.get(user=request.user)        
            x=doctor.finger
        else:
            pharmacist=Pharmacist.objects.get(user=request.user)
            x=pharmacist.finger
        
        if (request.user.is_doctor or request.user.is_pharmacist):
            print('Give Fingerprint')
            print(x)
            if give3(x):
                return HttpResponseRedirect('user')  

    return HttpResponseRedirect('user')
    return render(request,'test.html',{})

@method_decorator([login_required, doctor_required], name='dispatch')
class PrescriptionCreateView(generic.CreateView):
        
    model=Prescription 
    template_name='prescription_create.html'
    

    def get(self, request, *args, **kwargs):
        form =  PrescriptionModelForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = PrescriptionModelForm()               
        id_=request.session.get('id')
        doctor_=Doctor.objects.get(user=request.user)       
        prescription=Prescription.objects.create(title=request.POST['title'],prescription_text=request.POST['prescription_text'],date=request.POST['date'],patient=Patient.objects.get(id=id_))
        prescription.checked=False
        prescription.disease=request.POST['disease']
        prescription.medicine=request.POST['medicine']  
        prescription.doctor=doctor_
        prescription.save()       
        return render(request, self.template_name, {'form': form})

class PatientDetailView(generic.DetailView):

    model=Patient
    template_name='patient_search.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # context['id']=self.request.GET.get('q')
        return context
  
    
    def get_object(self):
        print('Read the Smart Card')
        print('')
        query = give3()
        # query=self.request.GET.get('q') 
        
        print(query) 
        try: 
            if query:
                object_= get_object_or_404(Patient,RFID=query)
                # object_=get_object_or_404(Patient,id=query)
                self.request.session['id']=object_.id  
                             
            else:
                object_ = None
        except Http404:
            object_ = None
        return object_
        
       
class DoctorSignUpView(generic.CreateView):
    
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class PharmacistSignUpView(generic.CreateView):
    
    model = User
    form_class = PharmacistSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Pharmacist'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class PatientSignUpView(generic.CreateView):
    
    model = User
    form_class = PatientSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(request=self.request)
        login(self.request, user)            
        return redirect('home')

@login_required
@doctor_required
def DoctorView(request,*args,**kwargs):
    obj=Doctor.objects.get(user=request.user)
    return render(request,'doctorview.html',{'doctor':obj})

@login_required
@patient_required
def PatientView(request):
    obj=Patient.objects.get(user=request.user)
    return render(request,'patientview.html',{'patient':obj})


class prescription_listview(generic.ListView):
    model=Prescription
    template_name='prescription_list.html'
    
    def get_queryset(self):
        id_=self.request.session['id']
        self.patient= get_object_or_404(Patient,id=id_)
        return Prescription.objects.filter(patient=self.patient)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient']=self.patient
        
        return context

class prescription_detailview(generic.DetailView):
    model=Prescription
    template_name='prescription_detail.html'
    
        
    def get_queryset(self):
        self.patient= get_object_or_404(Patient,id=self.request.session['id'])
        return Prescription.objects.filter(patient=self.patient)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient']=get_object_or_404(Patient,id=self.request.session['id'])
        return context
    
    def get_object(self):        
        obj = get_object_or_404(Prescription,id=self.kwargs.get('pk'))
        return obj

@login_required
@patient_required
def patient_prescription_view(request):
    patient=Patient.objects.get(user=request.user)
    request.session['id']=patient.id     
    p=get_object_or_404(Patient,id=request.session['id'])
    queryset=Prescription.objects.filter(patient=p)
    context={'prescription_list' : queryset, 'patient':p }
    return render(request,'prescription_list.html',context)

@method_decorator([login_required, doctor_required], name='dispatch')
class PatientDetailUpdateView(View):

    template_name='patient_update.html'   
    
    def get(self, request, *args, **kwargs):
        form =  PatientModelForm()
        
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        
        form = PatientModelForm(request.POST)              
        id_=request.session.get('id')
        print(id_)
        patient=Patient.objects.get(id=id_)
        d=dict(request.POST) 
        print(d)       
        allergy=d.get('allergy',None)
        genetic=d.get('genetic_disorder',None)
        patient.allergy.clear() 
        patient.genetic_disorder.clear()
        if allergy is not None:       
            for x in allergy:
                a=Allergy.objects.create(name=x)
                patient.allergy.add(a)
        if genetic is not None: 
            for x in genetic:
                a=Genetic_disorder.objects.create(name=x)
                patient.genetic_disorder.add(a)
        bg=d.get('blood_group',None)        
        
        patient.blood_group=bg[0]
        patient.save()
        return render(request, self.template_name, {'form': form})

@login_required
@pharmacist_required
def prescription_detail_view(request,*args,**kwargs):
    
    patient=Patient.objects.get(id=request.session.get('id'))    
    prescription=Prescription.objects.get(id=kwargs.get('pk'))
    
    prescription.checked=True
    prescription.save()
    print(prescription.checked)
    template='prescription_detail.html'    
    return render(request,template,{'prescription':prescription,'patient':patient})

@login_required
@patient_required
def mydoctorview(request):
    patient_=Patient.objects.get(user=request.user)
    pre=Prescription.objects.filter(patient=patient_)
    l=[]
    for x in pre:
        l.append(x.doctor)
    l=list(set(l))
    print(l)
    return render(request,'mydoctor.html',{'doctor_list':l})

    
    



 