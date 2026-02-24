from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from MahalApp.models import HomeSlider

def PartialsView(request):
    return render(request, 'admin/Partials.html')

@login_required
def home_slider_view(request):
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, 'Access Denied! Only superusers can access this page.')
        return redirect('dashboard')
    
    # Get or create HomeSlider object
    home, created = HomeSlider.objects.get_or_create(id=1)
    
    if request.method == "POST":
        # Get form data
        mahal_name = request.POST.get("mahal_name", "").strip()
        bg_color = request.POST.get("bg_color", "#ffffff")
        font_color = request.POST.get("font_color", "#000000")
        font_size = request.POST.get("font_size", "16")
        logo_radius = request.POST.get("logo_radius", "40")
        whatsapp_no=request.POST.get("whatsapp_no")
        phone=request.POST.get("phone")
        gmail=request.POST.get("gmail")
        # Validate required fields
        if not mahal_name:
            messages.error(request, 'Mahal name is required!')
            context = {'home': home}
            return render(request, 'admin/home_slider.html', context)
        
        # Update fields
        home.mahal_name = mahal_name
        home.bg_color = bg_color
        home.font_color = font_color
        home.font_size = font_size
        home.logo_radius = int(logo_radius) if logo_radius.isdigit() else 40
        home.whatsapp_no = whatsapp_no
        home.phone = phone
        home.gmail = gmail

        print(home.font_color)
        # Handle file upload
        if request.FILES.get("logo"):
            uploaded_file = request.FILES.get("logo")
            
            # Validate file type
            if not uploaded_file.content_type.startswith('image/'):
                messages.error(request, 'Please upload a valid image file (JPG, PNG, GIF)!')
                context = {'home': home}
                return render(request, 'admin/home_slider.html', context)
            
            # Validate file size (max 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, 'File size too large! Please upload an image smaller than 5MB.')
                context = {'home': home}
                return render(request, 'admin/home_slider.html', context)
            
            home.logo = uploaded_file
        
        # Save the object
        try:
            home.save()
            messages.success(request, 'Home slider settings updated successfully!')
            return redirect('home_slider')
        except Exception as e:
            messages.error(request, f'Error saving settings: {str(e)}')
    
    # Render form with current data
    context = {'home': home}
    return render(request, 'admin/home_slider.html', context)


from MahalApp.models import HomeBanner

@login_required
def home_banner_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied!")
        return redirect("dashboard")

    if request.method == "POST":
        image = request.FILES.getlist("image")
        title = request.POST.getlist("title")
        subtitle = request.POST.getlist("subtitle")

        if image:

            #Delete Old Banners
            HomeBanner.objects.all().delete()

            #create new Banners 

            for i in range(len(image)):
                  HomeBanner.objects.create(
                image=image[i],
                title=title[i],
                subtitle=subtitle[i]
            )
            messages.success(request, "Home Banner Is Created!")
            return redirect("home_banner")
        else:
            messages.error(request, "Image Is Required !")

    return render(request, "admin/home_banner.html")

