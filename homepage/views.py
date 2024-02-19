from django.shortcuts import render
from stressapp.models import userAttribute, friend_request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import sys
from django.http import JsonResponse
from llama2.llama2 import run_chatbot

# Create your views here.
def homepage(request):
    username = request.session.get('username', None)

    try:
        user = userAttribute.objects.get(username=username)

        if request.session.get_expiry_age() <= 0:
            request.session.pop('username', None)

    except userAttribute.DoesNotExist:
        return redirect("index")
    
    # if currently new user, set user to not new user
    isnewuser = user.new_user
    if isnewuser:
        user.new_user = False
        user.save()

    return render(request, 'homepage.html', {'username': username, 'newuser': isnewuser})


@login_required
def prompt_reciever(request):

    if request.method == 'POST':
        user = userAttribute.objects.get(username=request.session.get('username', None))
        user_interests = [instance.interest for instance in user.tags.all()]
        user_input = request.POST['user_input']
        
        if user_interests:
            prompt_interests = "My hobbies and music and movie interests are" + ", ".join(user_interests) + "."
        else:
            prompt_interests = ""

        if user_input == "Outside":
            prompt_inorout = " as well as some music to listen to."
        else:
            prompt_inorout = " as well as some music and a movie I could also watch."

        prompt = prompt_interests + "Give me an activity to do " + user_input + prompt_inorout

        response = run_chatbot(prompt)
        response_data = {'chatbot_response': response, 'prompt': prompt}
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'})

@login_required
def send_friend_request(request):
    if request.method == 'POST':
        from_user = userAttribute.objects.get(username=request.session.get('username', None))
        to_user = userAttribute.objects.get(username=request.POST['to_user'])
        if not to_user:
            # return error
            pass

        curr_friend_req, created = friend_request.objects.get_or_create(from_user=from_user, to_user=to_user)

@login_required
def accept_friend_request(request):
    curr_friend_req = friend_request.objects.get_or_create(id=request.POST['reqID'])
    if curr_friend_req.to_user == request.user:
        curr_friend_req.to_user.friends.add(curr_friend_req.from_user)
        curr_friend_req.from_user.friends.add(curr_friend_req.to_user)
        curr_friend_req.delete()
        return JsonResponse({'message': 'Friend request accepted!'})
    else:
        return JsonResponse({'message': 'Unable to accept friend request. :/'})
    
@login_required
def friends(request):
    return render(request, 'friends.html')
