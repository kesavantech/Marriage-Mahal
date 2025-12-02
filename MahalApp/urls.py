from django.urls import path

from . import views

urlpatterns=[
    path('',views.home_view,name='home'),
    path('login/',views.login_view,name='login'),
    path('about/',views.about_view,name='about'),
    path('contact/',views.contact_view,name='contact'),
    path('special/',views.special_view,name='special'),
    path("whatsapp/", views.whatsapp_greet, name="whatsapp_greet"),


    #partials
    path('header/',views.header_view, name='header'),
    path('header/',views.footer_view, name='footer'),

]
    # path('search/',views.search_view,name='search'),
    # path('booking_form/',views.booking_form_view,name='booking_form'),




