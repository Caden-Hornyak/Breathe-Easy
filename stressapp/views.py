from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .readdata import ReadData
from .models import userAttribute, interest
import sys


# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        
        username = request.POST['username'].strip()
        fullname = request.POST['fullname']
        email = request.POST['email']
        pass1 = request.POST['pass1'].strip()
        pass2 = request.POST['pass2']
        tags = request.POST['tags']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try some other username.")
            return redirect('index')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!")
            return redirect('index')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!")
            return redirect('index')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('index')
        
        # if user entered tag does not already exist, save it
        tagl = tags.split(',')
        for entered_tag in tagl:
            if not interest.objects.filter(interest=entered_tag).exists():   
                user_inter = interest(interest=entered_tag)
                user_inter.save()
        
        myuser = User.objects.create_user(username=username, password=pass1)
        userAttr = userAttribute(fullname=fullname, username=username, email=email)

        myuser.is_active = True
        myuser.save()
        userAttr.save()
        messages.success(request, "Your Account has been created succesfully!")

        
        return redirect('index')

    reader = ReadData(False)
    path = r"C:\Users\19494\Desktop\Coding\Python\StressManWeb\data\hobbies.txt"
    dic = reader.read_txt(path)
    return render(request, "signup.html", { "interest_key": dic})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            print(user.username, type(user.username), file=sys.stderr)
            return redirect(reverse('homepage', kwargs={'username': user.username}))
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('index')
        
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('index')