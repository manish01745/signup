from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from .forms import SignupForm
from django.contrib.auth.models import User
from .models import Patient, Doctor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            address_line1 = form.cleaned_data.get('address_line1')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            pincode = form.cleaned_data.get('pincode')
            user_type = request.POST.get('user_type')
            if user_type == 'Patient':
                patient = Patient.objects.create(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode)
                patient.save()
            elif user_type == 'Doctor':
                doctor = Doctor.objects.create(user=user, address_line1=address_line1, city=city, state=state, pincode=pincode)
                doctor.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'patient'):
                    return HttpResponseRedirect('patient_page')
                elif hasattr(user, 'doctor'):
                    return HttpResponseRedirect('doctor_page')
    else:
        fm=AuthenticationForm()
        return render(request, 'login.html',{"form":fm})
    
    
# def patient_page(request):
#     return render(request, 'patient_page.html')
        
        
        
# def doctor_page(request):
#     doctor = Doctor.objects.all()
#     return render(request, 'doctor_page.html',{'doctor': doctor})
    
    
    
    
    
    
    
def log_out(request):
    logout(request)
    return HttpResponseRedirect('login')


@login_required
def patient_page(request,id):
    patient = Patient.objects.get(pk=id)
    return render(request, 'patient_page.html', {'patient': patient})

@login_required
def doctor_page(request,id):
    doctor = Doctor.objects.get(pk=id)
    return render(request,'doctor_page.html', {'doctor': doctor})