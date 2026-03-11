from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import LoginSerializer 
from MahalApp.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_exempt
"""
@csrf_exempt என்ன சொல்கிறது என்றால்:

இந்த view-க்கு CSRF check செய்ய வேண்டாம்.

ஏன் என்றால்:

mobile app

Postman

React frontend

இவை CSRF token அனுப்பாது.


"""
def api_login(request):
    
    if request.method == "POST":
    #request.data என்பது client request body-ல் அனுப்பும் data.
    #அது JSON / form-data / multipart data ஆக இருக்கலாம்.
        serializer = LoginSerializer(data=request.data)
        print(f"Serializer: {serializer}")

        if not serializer.is_valid():
            return Response(serializer.errors)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    try:
        user = User.objects.get(email = email)
    except User.DoesNotExist:
        return Response({
            "error":"Invalid Email !"
        })
    user = authenticate(username=user.username, password=password)

    if user is None:
        return Response({"error":"invalid pasdsword !"})
    
    login(request,user)

    return Response({
        "message":"Login Successfully !",
        "Username":user.username,
        "Email":user.email,
        "Role":user.role
    })