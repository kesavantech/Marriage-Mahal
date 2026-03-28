from django.urls import path, include

from . import views

urlpatterns=[

    ########   GLOBAL URL ##########
    path('',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path("booking_details/", views.booking_details_view, name="booking_details"),
    #API URL
    path('api/', include('MahalApp.api.urls')),
    
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('profile/',views.profile_view, name='profile'),
    path('about/',views.about_view,name='about'),
    path('contact/',views.contact_view,name='contact'),
    path('special/',views.special_view,name='special'),
    path("whatsapp/", views.whatsapp_greet, name="whatsapp_greet"),
    path('logout/', views.logout_view, name='logout'),

    #partials
    path('header/',views.header_view, name='header'),
    path('footer/',views.footer_view, name='footer'),

    ######    ADMIN URL   ##################
    path("admin_base_view/", views.admin_base_view, name="admin_base_view"),
    path('Partials/',views.PartialsView, name='Partials'),
    path('home_slider/', views.home_slider_view, name='home_slider'),
    path('home_banner/', views.home_banner_view, name='home_banner'),
    path("users/", views.users_view, name='users'),
    path("change_action/<int:user_id>/",views.change_action,name="change_action"),
    path("add_manager/",views.add_manager_view, name="add_manager"),

    ######    CLIENT URL   ##################
    path('booking/', views.booking_form_view, name='booking_form'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),

    ######    MANAGER URL   ##################
    path('manage-bookings/', views.manage_bookings_view, name='manage_bookings'),
    path('confirm-booking/<int:booking_id>/', views.confirm_booking_view, name='confirm_booking'),
    path('reject-booking/<int:booking_id>/', views.reject_booking_view, name='reject_booking'),
    path('mark-advance-paid/<int:booking_id>/', views.mark_advance_paid_view, name='mark_advance_paid'),
    
]





