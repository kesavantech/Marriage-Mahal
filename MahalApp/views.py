from django.shortcuts import render, redirect
import requests
# Create your views here.
from django.http import HttpResponse

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

def login_view(request):
    return render(request,'login.html')

def special_view(request):
    return render(request,'special.html')

def contact_view(request):
    return render(request,'contact.html')

from django.shortcuts import redirect

def whatsapp_greet(request):
    phone_number = "919342532503"  # Your WhatsApp number
    message = "Vanakkam 🙏, Welcome to Muthukumaran Mahal! How can we help you?"
    whatsapp_url = f"https://wa.me/{phone_number}?text={message}"
    return redirect(whatsapp_url)



def header_view(request):
    return render(request, 'partials/header.html')


def footer_view(request):
    return render(request, 'partials/footer.html')
