from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Profile
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.core.files.storage import default_storage
import asyncio
from deepgram import Deepgram


from HCT.settings import DEEPGRAM_API_KEY

# Create your views here.


def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')    
     

#ACCOUNT VIEWS

def register(request):
    user_form = UserRegistrationForm(request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'dashboard.html')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'edit.html', {'user_form': user_form, 'section': 'edit'})



#SECURITY VIEWS


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def transcribe(request):
    return render(request, 'speech_translate.html')


async def transcribe_audio(file_path):
    deepgram = Deepgram(DEEPGRAM_API_KEY)

    with open(file_path, "rb") as audio:
        source = {"buffer": audio, "mimetype": "audio/wav"}

        response = await deepgram.transcription.prerecorded(source, {"punctuate": True})
    
    # Extract transcript
    transcript = response.get("results", {}).get("channels", [])[0].get("alternatives", [])[0].get("transcript", "")
    
    return transcript

@login_required
@csrf_exempt
def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
            
        # Save the file temporarily
        file_path = default_storage.save(f'audio/{audio_file.name}', audio_file)

        # Convert audio file to text using Deepgram
        transcript = asyncio.run(transcribe_audio(file_path))

        return JsonResponse({'message': 'Audio uploaded successfully', 'transcript': transcript})

    return JsonResponse({'error': 'Invalid request'}, status=400)

"""
@login_required
@csrf_exempt
def transcribe_audios(request):
    if request.method == 'POST':
        # Get the audio file from the POST request
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return JsonResponse({'error': 'No audio file provided'}, status=400)

        # Send audio file to Deepgram API for transcription
        response = requests.post(
            'https://api.deepgram.com/v1/listen',
            headers={'Authorization': f'Token {DEEPGRAM_API_KEY}'},
            files={'file': audio_file},
            data={'model': 'general'}
        )

        # Check if the request was successful
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to get transcription'}, status=response.status_code)

        transcription_result = response.json()
        transcription_text = transcription_result.get('results', {}).get('channels', [])[0].get('alternatives', [])[0].get('transcript', '')

        return JsonResponse({'transcription': transcription_text})

    return JsonResponse({'error': 'Invalid request method'}, status=405)


"""

