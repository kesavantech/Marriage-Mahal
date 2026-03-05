from django.urls import path

from . import views

urlpatterns=[

    ########   GLOBAL URL ##########
    path('',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
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
    path('Partials/',views.PartialsView, name='Partials'),
    path('home_slider/', views.home_slider_view, name='home_slider'),
    path('home_banner/', views.home_banner_view, name='home_banner'),
    path("users/", views.users_view, name='users'),
    path("update_user_profile/<int:user_id>/", views.update_user_profile_view, name="update_user_profile_view"),

]





