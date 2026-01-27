from django.shortcuts import render, redirect
import requests

def HomeSliderView(request):
    return render(request, 'admin/HomeSlider.html')