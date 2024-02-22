from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.urls import reverse
from .readdata import ReadData
from .models import userAttribute, interest
import sys


# Create your views here.
def index(request):

    if 'side' in request.session:
        side = request.session.get('side', None)
        request.session.pop('side', None)
    else:
        side = 'middle'

    return render(request, "index.html", {'side': side})

def register(request):

    if request.method == "POST":
        
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        tags = request.POST['tags']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            request.session['side'] = 'left'
            return redirect('index')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already has an account!")
            request.session['side'] = 'left'
            return redirect('index')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!")
            request.session['side'] = 'left'
            return redirect('index')
        
        # if not username.isalnum():
        #     messages.error(request, "Username must be Alpha-Numeric!")
        #     request.session['side'] = 'left'
        #     return redirect('index')
        
        # if user entered tag does not already exist, save it
        tagl = tags.split(',')
        for entered_tag in tagl:
            if not interest.objects.filter(interest=entered_tag).exists():   
                user_inter = interest(interest=entered_tag)
                user_inter.save()
        
        myuser = User.objects.create_user(username=username, password=pass1)
        userAttr = userAttribute(username=username, email=email)

        myuser.is_active = True
        myuser.save()
        userAttr.save()
        messages.success(request, "Your Account has been created succesfully!")

        
        return redirect('index')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        remember_me = 'remember_me' in request.POST

        
        user = authenticate(username=username, password=pass1)
        if user is not None:

            auth_login(request, user)
            request.session['username'] = username

            # if user wants to be remembered set expiry for 2 weeks else None
            if remember_me:
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)
            
            user_atr = userAttribute.objects.get(username=username)
            user_atr.active = True
            user_atr.save()
            return redirect(reverse('homepage'))
        else:
            messages.error(request, "Bad Credentials!")
            request.session['side'] = 'right'
            return redirect('index')
        
    return render(request, 'login.html')

def signout(request):
    user_atr = userAttribute.objects.get(username=request.session.get('username', None))
    user_atr.active = True
    user_atr.save()
    logout(request)
    
    return redirect('index')


        
