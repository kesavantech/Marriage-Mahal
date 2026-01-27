from django.shortcuts import render, redirect
import requests

def PartialsView(request):
    return render(request, 'admin/Partials.html')