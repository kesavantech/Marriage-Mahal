from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from MahalApp.models import User, HomeBanner, Booking
from django.contrib.auth.decorators import login_required


def home_view(request):
    from MahalApp.models import HomeSlider
    home_banner=HomeBanner.objects.all()
    for i in home_banner:
        print(f"HomeImage:{i.image}")
        print(f"HomeTitle:{i.title}")
        print(f"HomeSubitle:{i.subtitle}")
    context={
        "home_banner":home_banner
    }
    return render(request, 'home.html', context)

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
        profile = None
        if request.FILES.get("profile"):
            profile = request.FILES.get("profile")

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
            password=password1, profile = profile
            )
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


    
@login_required
def dashboard_view(request):
    context = {}
    if request.user.role in ['admin', 'manager']:
        context['all_users'] = User.objects.all()
        context['total_users'] = User.objects.count()
    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get("phone", user.phone)
        user.address = request.POST.get("address", user.address)
        
        # Handle profile image upload with validation
        if request.FILES.get("profile"):
            uploaded_file = request.FILES.get("profile")
            
            # Validate file type
            if not uploaded_file.content_type.startswith('image/'):
                messages.error(request, 'Please upload a valid image file!')
                return redirect('profile')
            
            # Validate file size (max 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, 'File size too large! Max 5MB allowed.')
                return redirect('profile')
            
            user.profile = uploaded_file
        
        # Handle password change
        old_password = request.POST.get("old_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
    
        if new_password or confirm_password:
            if not old_password:
                messages.error(request, "Please Enter Your Old Password !")
                return redirect('profile')

            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect !")
                return redirect('profile')

            if new_password != confirm_password:
                messages.error(request, "New Password and Confirm Password do not match !")
                return redirect('profile')
            
            user.set_password(new_password)
        
        # Save all changes once
        user.save()
        messages.success(request, 'Profile Updated Successfully !')
        return redirect('profile')
    
    context = {'user': user}
    return render(request, 'profile.html', context)

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


@login_required
def booking_form_view(request):
    if request.user.role != 'client':
        messages.error(request, 'Only clients can make bookings!')
        return redirect('dashboard')

    if request.method == 'POST':
        event_date = request.POST.get('event_date')
        event_type = request.POST.get('event_type')
        hall_type = request.POST.get('hall_type')
        guest_count = request.POST.get('guest_count')
        special_requests = request.POST.get('special_requests', '')
        payment_screenshot = request.FILES.get('payment_screenshot')

        if not payment_screenshot:
            messages.error(request, 'Please upload your payment screenshot!')
            return redirect('booking_form')

        if Booking.objects.filter(event_date=event_date, status='Confirmed').exists():
            messages.error(request, 'This date is already booked! Please choose another date.')
            return redirect('booking_form')

        if Booking.objects.filter(event_date=event_date, status='Pending').exists():
            messages.warning(request, 'This date already has a pending booking. You are added to the waiting list. Your advance will be refunded if the date is not available.')

        Booking.objects.create(
            user=request.user,
            event_date=event_date,
            event_type=event_type,
            hall_type=hall_type,
            guest_count=guest_count,
            special_requests=special_requests,
            payment_screenshot=payment_screenshot
        )
        messages.success(request, 'Booking submitted! We will verify your payment and confirm shortly.')
        return redirect('my_bookings')

    context = {
        'event_choices': Booking.event_choices,
        'hall_choices': Booking.hall_choices,
        'event_prices': Booking.EVENT_PRICES,
        'ac_extra': Booking.AC_EXTRA,
    }
    return render(request, 'booking_form.html', context)