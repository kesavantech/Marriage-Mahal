from django.urls import path

from . import views
from .views.admin_views import PartialsView

urlpatterns=[

    ########   GLOBAL URL ##########
    path('',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('about/',views.about_view,name='about'),
    path('contact/',views.contact_view,name='contact'),
    path('special/',views.special_view,name='special'),
    path("whatsapp/", views.whatsapp_greet, name="whatsapp_greet"),
    path('logout/', views.logout_view, name='logout'),


    #partials
    path('header/',views.header_view, name='header'),
    path('footer/',views.footer_view, name='footer'),

    ######    ADMIN URL   ##################
    path('Partials/',PartialsView, name='Partials'),
]





