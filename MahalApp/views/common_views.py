from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from MahalApp.models import User

def home_view(request):
    return render(request,'home.html')

def about_view(request):
    api_key="f586208ffb5bf58837c78e0f4ce0a04a"
    latitude=11.046438148728702
    longitude=77.430913146049
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"

    response=requests.get(url)
    data=response.json()

    weather_data={}
    if response.status_code==200:
        weather_data={
            'location':'Peruntholuvu. Tirupur',
            'temperature':data['main']['temp'],
            'description':data['weather'][0]['description'],
            'icon':data['weather'][0]['icon']
        }

    return render(request,'about.html',{'weather':weather_data})

def register_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        role=request.POST.get('role')
        address=request.POST.get('address')
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email Is Already Exist !')
            return redirect('register')

        if password!=password1:
            messages.error(request, 'Both Password Not Match !')
            return redirect('register')

        if User.objects.filter(phone=phone).exists():
            messages.error(request,'phone number is already exist!')
            return redirect('register')

        User.objects.create_user(
            username=username, email=email, phone=phone, role=role, address=address,
            password=password1)
        messages.success(request,'You Are Register Successfully !')
        return redirect('login')
    return render(request,'register.html')

def login_view(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "Invalid Email !")
            return redirect('login')
    
        user=authenticate(request, username=user.username, password=password)
            
        if user is None:
            messages.error(request,'Invalid Password !')
            return redirect('login')
        
        login(request, user)
        messages.success(request,f'Login SuccesFully')
        return redirect('dashboard')

    return render(request,'login.html')

def dashboard_view(request):
    if request.user.role == 'admin':
        all_users = User.objects.all()
        return render(request, 'dashboard.html', {'all_users': all_users})
    return render(request, 'dashboard.html')

def special_view(request):
    return render(request,'special.html')

def contact_view(request):
    return render(request,'contact.html')

def whatsapp_greet(request):
    phone_number = "919342532503"
    message = "Vanakkam 🙏, Welcome to Muthukumaran Mahal! How can we help you?"
    whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
    return redirect(whatsapp_url)

def header_view(request):
    return render(request, 'partials/header.html')

def footer_view(request):
    return render(request, 'partials/footer.html')

def logout_view(request):
    logout(request)
    return redirect('login')