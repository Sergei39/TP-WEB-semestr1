from django.shortcuts import render

# Create your views here.

questions = [
    {
        'id': idx,
        'title': f'My best question {idx}',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur... ',
    } for idx in range(10)
]


def index(request):
    return render(request, 'index.html', {
        'questions': questions,
    })


def hot(request):
    return render(request, 'hot.html', {
        'questions': questions,
    })


def ask(request):
    return render(request, 'ask.html', {})


def login(request):
    return render(request, 'login.html', {})


def question(request, pk):
    question = questions[pk]
    return render(request, 'question.html', {
        'question': question,
    })


def settings(request):
    return render(request, 'settings.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def tag(request, tagname):
    return render(request, 'tag.html', {
        'questions': questions,
        'tagname': tagname,
    })
