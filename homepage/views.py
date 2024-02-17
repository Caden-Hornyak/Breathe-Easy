from django.shortcuts import render
from stressapp.models import userAttribute
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


def ajax_view(request):

    if request.method == 'POST':
        user = userAttribute.objects.get(username=request.session.get('username', None))
        user_interests = [instance.interest for instance in user.tags.all()]
        user_input = request.POST['user_input']
        prompt = "I like " + ", ".join(user_interests) + ". Give me something to do " + user_input + ". Respond concise."

        response = run_chatbot(prompt)
        response_data = {'chatbot_response': response, 'prompt': prompt}
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'})