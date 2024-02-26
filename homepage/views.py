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
            prompt_inorout = " as well as 3 music artistics to listen to."
        else:
            prompt_inorout = " as well as 3 music artistics to listen to and 1 movie I could watch."

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
            return JsonResponse({'response': 'User does not exist', 'added': 'false'})

        if len(friend_request.objects.filter(to_user=to_user, from_user=from_user)) > 0:
            return JsonResponse({'response': 'Friend request already sent', 'added': 'false'})

        curr_friend_req = friend_request(from_user=from_user, to_user=to_user)
        curr_friend_req.save()
        if (from_user.username == to_user.username):
            return JsonResponse({'response': 'You sent a friend request to yourself...', 'added': 'true'})
        else:
            return JsonResponse({'response': 'Friend request sent', 'added': 'true'})

@login_required
def accept_friend_request(request):
    if request.method == 'POST':
        action = request.POST['action']
        curr_friend_req = friend_request.objects.get(id=request.POST['reqID'])
        if curr_friend_req.to_user == request.user:
            if action == 'accept':
                curr_friend_req.to_user.friends.add(curr_friend_req.from_user)
                curr_friend_req.from_user.friends.add(curr_friend_req.to_user)
            curr_friend_req.delete()

            if action == 'accept':
                return JsonResponse({'response': 'Friend request accepted!'})
            else:
                return JsonResponse({'response': 'Friend request rejected!'})
        else:
            return JsonResponse({'response': 'Unable to accept friend request. :/'})
    
@login_required
def get_friend_request(request):
    friend_requests = friend_request.objects.filter(to_user=userAttribute.objects.get(username=request.session.get('username', None)))
    users = []
    for curr_friend_request in friend_requests:
        try:
            user = userAttribute.objects.get(username=curr_friend_request.from_user)
        except userAttribute.DoesNotExist:
            return JsonResponse({'response': 'Invalid friend request.'})
        
        users.append([user.username, user.profile_picture.url, curr_friend_request.id])

    return JsonResponse({'friend_requests': users})

    
@login_required
def friends(request):
    user = userAttribute.objects.get(username=request.session.get('username', None))

    return JsonResponse({'friends': [[friend.username, friend.profile_picture.url, friend.is_active] for friend in user.friends.all()]})

@login_required
def get_chats(request):
    username = request.session.get('username', None)
    user = userAttribute.objects.get(username=username)
    chats = []
    for chat in user.chats.all():
        participants = [participant for participant in chat.participants.all() if participant.username != username]
        if len(participants) > 1:
            prof_pic = '/media/default_groupchat.png'
        else:
            prof_pic = participants[0].profile_picture.url

        chat_name = ', '.join([participant.username for participant in participants])
        chats.append([chat.id, chat_name, prof_pic[1:], chat.date_created.strftime('%m/%d/%Y')])

    return JsonResponse({'chats': chats})


# If chat with matching participants exists, return it, else create new chat and return it
@login_required
def create_chat(request):   
    if request.method == 'POST':
        participants = json.loads(request.POST['friends']) + [request.session.get('username', None)]
        curr_chats = chat.objects.filter(participants__username__in=participants).distinct()

        # Convert the participants list to a set for easy comparison
        participants_set = set(participants)

        for curr_chat in curr_chats:
            # Get the participants of the current chat
            existing_participants = list(curr_chat.participants.all())

            # Convert the existing participants list to a set for comparison
            existing_participants_set = set(existing_participants)

            # Check if the sets are equal
            if participants_set == existing_participants_set:
                return JsonResponse({'chat': curr_chat.id})
        else:

            new_chat = chat()
            new_chat.save()
            for user in [userAttribute.objects.get(username=participant) for participant in participants]:
                new_chat.participants.add(user)
                user.chats.add(new_chat)
                user.save()

            new_chat.save()
            return JsonResponse({'chat': new_chat.id})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

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

@login_required
def premium(request):
    return render(request, 'premium.html')