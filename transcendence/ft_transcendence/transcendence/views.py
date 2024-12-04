from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, Score, Room
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "pong_app/index.html")

def calculator(request):
    return render(request, 'pong_app/calculator.html', {})

def chat_view(request):
    return render(request, 'pong_app/chat.html')

def login_view(request):
    if (request.user.is_authenticated):
        return redirect('index')
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "pong_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "pong_app/login.html")

def register(request):
    if (request.user.is_authenticated):
        return redirect('index')
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "pong_app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            score_entry = Score.objects.create(user=user, score=10)
            score_entry.save()
        except IntegrityError:
            return render(request, "pong_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('index')
    else:
        return render(request, "pong_app/register.html")


def account(request, user_id):
    user = User.objects.get(pk=user_id)
    score = Score.objects.get(user=user)

    return render(request, "pong_app/account.html", {
        "username": user.username,
        "score": score.score,
        "user_account": user,
    })
def logout_view(request):
    logout(request)
    return redirect("index")

def pong(request):
    return render(request, 'pong_app/pong.html')

@login_required(login_url='/login/')
def room(request, room_name):
    return render(request, 'pong_app/room.html', {'room_name': room_name})

def bot(request):
    return render(request, 'pong_app/bot.html')

def chat(request):
    return render(request, 'pong_app/chat.html')
