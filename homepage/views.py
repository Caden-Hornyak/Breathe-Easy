from django.shortcuts import render
from stressapp.models import userAttribute
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import sys

# Create your views here.
def homepage(request, **kwargs):
    
    try:
        user = userAttribute.objects.get(username=kwargs['username'])
    except userAttribute.DoesNotExist:
        return redirect("index")
    
    # if currently new user, set user to not new user
    isnewuser = user.new_user
    print(isnewuser, file=sys.stderr)
    if isnewuser:
        user.new_user = False
        user.save()

    return render(request, 'homepage.html', {'username': kwargs['username'], 'newuser': isnewuser})