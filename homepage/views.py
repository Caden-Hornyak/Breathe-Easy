from django.shortcuts import render
from stressapp.models import userAttribute, friend_request, chat, message
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import sys
from django.http import JsonResponse
from llama2.llama2 import run_chatbot
import json


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

    return render(request, 'homepage.html', {'username': username, 'newuser': isnewuser, 'prof_pic': user.profile_picture.url,
                                             'tags': [instance.interest for instance in user.tags.all()]})


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
        try:
            from_user = userAttribute.objects.get(username=request.session.get('username', None))
            to_user = userAttribute.objects.get(username=request.POST['to_user'])
        except userAttribute.DoesNotExist:
            return JsonResponse({'response': 'User does not exist'})

        curr_friend_req, created = friend_request.objects.get_or_create(from_user=from_user, to_user=to_user)
        if (from_user.username == to_user.username):
            return JsonResponse({'response': 'You sent a friend request to yourself...'})
        else:
            return JsonResponse({'response': 'Friend request sent'})

@login_required
def accept_friend_request(request):
    curr_friend_req = friend_request.objects.get_or_create(id=request.POST['reqID'])
    if curr_friend_req.to_user == request.user:
        curr_friend_req.to_user.friends.add(curr_friend_req.from_user)
        curr_friend_req.from_user.friends.add(curr_friend_req.to_user)
        curr_friend_req.delete()
        return JsonResponse({'response': 'Friend request accepted!'})
    else:
        return JsonResponse({'response': 'Unable to accept friend request. :/'})
    
@login_required
def friends_page(request):
    user = userAttribute.objects.get(username=request.session.get('username', None))
    return render(request, 'friends.html', {'prof_pic': user.profile_picture.url, 'username': user.username})

@login_required
def friends(request):
    user = userAttribute.objects.get(username=request.session.get('username', None))
    return JsonResponse({'friends': [[friend.username, friend.profile_picture.url] for friend in user.friends.all()]})

@login_required
def get_chats(request):
    username = request.session.get('username', None)
    user = userAttribute.objects.get(username=username)
    chats = []
    for chat in user.chats.all():
        participants = [participant for participant in chat.participants.all() if participant.username != username]
        if len(participants) > 1:
            prof_pic = '/static/media/default_groupchat.png'
        else:
            prof_pic = participants[0].profile_picture.url

        chat_name = ', '.join([participant.username for participant in participants])
        chats.append([chat.id, chat_name, prof_pic[1:], chat.date_created.strftime('%m/%d/%Y')])

    return JsonResponse({'chats': chats})

@login_required
def create_chat(request):   
    if request.method == 'POST':
        participants = request.POST['usernames']
        if chat.objects.filter(participants=participants).exists():
            return chat.objects.filter(participants=participants).id
        
        new_chat = chat(participants=participants)
        new_chat.save()
        return new_chat.id

@login_required
def message_action(request):
    if request.method == 'POST':
        chat_id = request.POST['chat_id']
        action = request.POST['action']
        user = userAttribute.objects.get(username=request.session.get('username', None))

        try:
            curr_chat = chat.objects.get(id=chat_id)
        except chat.DoesNotExist:
            return JsonResponse({'response': 'Chat does not exist.'})
        

        if action == 'get':
            message_l = curr_chat.chat_messages.order_by('-date_created')[:50:-1]
            return JsonResponse({'messages': [[message.text, message.user.username == user.username] for message in message_l]})
        
        
        if action == 'destroy':
            message_id = request.POST['message_id']
            try:
                message_to_delete = curr_chat.messages.get(id=message_id)
            except message.DoesNotExist:
                return JsonResponse({'response': 'Unable to find message'})
            
            message_to_delete.delete()
        elif action == 'create':
            new_message = message(user=userAttribute.objects.get(username=request.session.get('username', None)),
                                   text=request.POST['text'])
            new_message.save()
            curr_chat.chat_messages.add(new_message)
            curr_chat.save()
            
            return JsonResponse({'messages': 'Message Created'})
        else:
            return JsonResponse({'response': 'Invalid Message Action'})

    return JsonResponse({'messages': 'Invalid HTTP request to message_action'})
