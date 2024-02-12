from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .readdata import ReadData

# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('index')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!")
            return redirect('index')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!")
            return redirect('index')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!")
            return redirect('index')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('index')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!")

        
        return redirect('signin')

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
            fname = user.first_name
            return render(request, "index.html")
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('index')
        
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('index')