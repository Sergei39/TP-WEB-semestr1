from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import random
import itertools


# Create your views here.

questions = [
    {
        'id': idx,
        'title': f'My best question {idx}',
        'like': random.randint(-5, 5),
        'answer': random.randint(0, 5),
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur... ',
    } for idx in range(20)
]

answers = [
    {
        'id': idx,
        'title': f'answer {idx}',
        'like': random.randint(-5, 5),
        'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat... ',
    } for idx in range(7)
]

def paginate(request, object_list, per_page=7):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    page_obj = paginate(request, questions)
    return render(request,'index.html', {
        'questions':page_obj,
        'page_obj': page_obj
    })


def hot(request):
    page_obj = paginate(request, questions)
    return render(request,'hot.html', {
        'questions':page_obj,
        'page_obj': page_obj
    })


def ask(request):
    return render(request, 'ask.html', {})


def login(request):
    return render(request, 'login.html', {})


def question(request, pk):
    question = questions[pk]
    this_answers = answers[:question.get('answer')]
    page_obj = paginate(request, this_answers)
    return render(request, 'question.html', {
        'question': question,
        'answers': page_obj,
        'page_obj': page_obj,
    })


def settings(request):
    return render(request, 'settings.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def tag(request, tagname):
    page_obj = paginate(request, questions)
    return render(request, 'tag.html', {
        'questions':page_obj,
        'page_obj': page_obj,
        'tagname': tagname,
    })
