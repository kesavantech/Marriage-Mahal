from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from MahalApp.models import User, HomeBanner, Booking
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Min, Max, Avg, Count

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

def booking_details_view(request):
    import calendar
    import math
    from datetime import date

    def moon_phase(d):
        """Returns moon age in days (0=new moon, ~15=full moon, ~29.5=next new moon)"""
        # Known new moon reference: Jan 6, 2000
        known_new_moon = date(2000, 1, 6)
        lunar_cycle = 29.53058867
        delta = (d - known_new_moon).days
        age = delta % lunar_cycle
        return age

    def get_day_info(d):
        age = moon_phase(d)
        weekday = d.weekday()  # 0=Mon, 6=Sun
        moon = None
        if age <= 1.5 or age >= 28.0:
            moon = 'amavasai'
        elif 13.5 <= age <= 16.0:
            moon = 'pournami'
        muhurtham = weekday in [2, 3, 4] and moon != 'amavasai'
        return {'moon': moon, 'muhurtham': muhurtham}

    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # Bookings for this month
    bookings = Booking.objects.filter(event_date__year=year, event_date__month=month).values('event_date', 'status')
    STATUS_PRIORITY = {'Confirmed': 1, 'Pending': 2, 'Rejected': 3, 'Cancelled': 4}
    date_status = {}
    for b in bookings:
        d = b['event_date']
        s = b['status']
        if d not in date_status or STATUS_PRIORITY.get(s, 9) < STATUS_PRIORITY.get(date_status[d], 9):
            date_status[d] = s

    # Tamil date calculation (approximate: Tamil month starts ~mid-April)
    # Simple approach: offset from a known Tamil new year
    from datetime import date as date_cls, timedelta
    TAMIL_NEW_YEAR_2025 = date_cls(2025, 4, 14)  # சித்திரை 1, 2025
    TAMIL_NEW_YEAR_2024 = date_cls(2024, 4, 14)
    TAMIL_NEW_YEAR_2026 = date_cls(2026, 4, 14)

    def get_tamil_date(d):
        # Pick the correct Tamil new year reference
        for tny in [date_cls(2026,4,14), date_cls(2025,4,14), date_cls(2024,4,14), date_cls(2023,4,14)]:
            if d >= tny:
                offset = (d - tny).days
                break
        else:
            offset = (d - date_cls(2023,4,14)).days

        TAMIL_MONTH_DAYS = [31,31,31,31,31,31,30,30,30,30,30,29]
        TAMIL_MONTH_NAMES = ['சித்திரை','வைகாசி','ஆனி','ஆடி','ஆவணி','புரட்டாசி',
                             'ஐப்பசி','கார்த்திகை','மார்கழி','தை','மாசி','பங்குனி']
        m = 0
        while m < 12 and offset >= TAMIL_MONTH_DAYS[m]:
            offset -= TAMIL_MONTH_DAYS[m]
            m += 1
        return TAMIL_MONTH_NAMES[m % 12], offset + 1

    # Build calendar with day info
    cal = calendar.monthcalendar(year, month)
    cal_with_info = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': 0, 'labels': [], 'status': None})
            else:
                d = date(year, month, day)
                t_month, t_day = get_tamil_date(d)
                week_data.append({
                    'day': day,
                    'tamil_date': f'{t_month} {t_day}',
                    'moon': get_day_info(d)['moon'],
                    'muhurtham': get_day_info(d)['muhurtham'],
                    'status': date_status.get(d),
                    'is_today': d == today,
                })
        cal_with_info.append(week_data)

    # Tamil month names (aligned: April=சித்திரை)
    TAMIL_MONTHS = [
        'தை', 'மாசி', 'பங்குனி', 'சித்திரை', 'வைகாசி', 'ஆனி',
        'ஆடி', 'ஆவணி', 'புரட்டாசி', 'ஐப்பசி', 'கார்த்திகை', 'மார்கழி'
    ]
    tamil_month = TAMIL_MONTHS[(month - 4) % 12]

    prev_month = month - 1 if month > 1 else 12
    prev_year  = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year  = year if month < 12 else year + 1

    ENGLISH_MONTHS = ['January','February','March','April','May','June',
                      'July','August','September','October','November','December']

    context = {
        'cal': cal_with_info,
        'year': year,
        'month': month,
        'month_name': ENGLISH_MONTHS[month - 1],
        'tamil_month': tamil_month,
        'today': today,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'booking_details.html', context)

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
        context['total_booking'] = Booking.objects.all().count()
        total_revenue = Booking.objects.aggregate(total=Sum('total_amount'))
        context['total_revenue'] = total_revenue['total'] or 0

        event_counts = (
            Booking.objects
            .values('event_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        context['event_labels'] = [e['event_type'] for e in event_counts]
        context['event_data']   = [e['count']      for e in event_counts]

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
    from MahalApp.models import HomeSlider, ContactMessage
    home = HomeSlider.objects.first()
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and phone and message:
            ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
            messages.success(request, 'Your message has been successfully sent. We will get back to you shortly.')
        else:
            messages.error(request, 'Please fill all fields.')
        return redirect('contact')
    return render(request, 'contact.html', {'home': home})

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