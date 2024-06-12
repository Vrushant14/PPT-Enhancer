import base64
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .backend import process_ppt
from django.conf import settings
import os
from bson import ObjectId  
from django.template.response import TemplateResponse
import pymongo
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from . tokens import generate_token
from pymongo import MongoClient
import mimetypes
from django.contrib.auth.hashers import make_password


client = pymongo.MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]
collection = db['enhanced_ppt']

def upload_ppt(request):
    if request.method == 'POST':
        username = request.session.get('username')

        if username:
            ppt_file = request.FILES.get('ppt_file')
            
            if ppt_file:
                try:
                    with open('temp.pptx', 'wb') as f:
                        for chunk in ppt_file.chunks():
                            f.write(chunk)
                    
                    enhanced_ppt_path = process_ppt('temp.pptx', username)
                    with open(enhanced_ppt_path, 'rb') as f:
                        enhanced_ppt_data = f.read()
                        ppt_doc = {'name': 'enhanced_presentation.pptx', 'data': enhanced_ppt_data, 'user': username}
                        result = collection.insert_one(ppt_doc)
                        inserted_id = result.inserted_id    
                    
                    os.remove('temp.pptx')
                    current_ppt = collection.find({'_id': inserted_id})
                    modified_ppts = []
                    for ppt in current_ppt:
                        ppt['str_id'] = str(ppt['_id'])
                        modified_ppts.append(ppt)
                    return render(request, 'current.html', {'current_ppt': modified_ppts})
                except Exception as e:
                    return HttpResponse(f"An error occurred: {str(e)}", status=500)
        else:
            return redirect('login')
    return render(request, 'page.html')

def view_past_ppts(request):
        username = request.session.get('username')

        if username:
            past_ppts = collection.find({'user': username})
            modified_ppts = []
            for ppt in past_ppts:
                ppt['str_id'] = str(ppt['_id'])
                modified_ppts.append(ppt)

            return render(request, 'past.html', {'past_ppts': modified_ppts})

        else:
            return redirect('login')

def entry(request: HttpRequest):
    return render(request, 'entry.html')

def about(request: HttpRequest):
    return render(request, 'about.html')

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]
user_collection = db['users']
collection = db['enhanced_ppt']

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        
        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }
        try:
            user_collection.insert_one(user_data)
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Failed to create account: {str(e)}')
            return redirect('signup')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_data = user_collection.find_one({'username': username, 'password': password})
        if user_data:
                request.session['username'] = username
                messages.success(request, 'You are now logged in.')
                return redirect('entry')  

        messages.error(request, 'Invalid username or password.')
        return redirect('login')

    return render(request, 'login.html')

def download_presentation(request, presentation_id):
    presentation = collection.find_one({'_id': ObjectId(presentation_id)})

    if presentation:
        presentation_data = presentation['data']
        filename = presentation['name']

        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = 'application/octet-stream'

        response = HttpResponse(presentation_data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponseNotFound('Presentation not found')
