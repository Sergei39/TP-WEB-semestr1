from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def ask(request):
    return render(request, 'ask.html', {})


def login(request):
    return render(request, 'login.html', {})


def question(request):
    return render(request, 'question.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def tag(request):
    return render(request, 'tag.html', {})
