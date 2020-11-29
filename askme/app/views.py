from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from app.models import Profile, Question, Answer, Tag, LikeAnswer, LikeQuestion
import itertools
from django.contrib import auth
from app.forms import LoginForm, AskForm



def paginate(request, object_list, per_page=10):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    questions = Question.objects.last_questions()
    page_obj = paginate(request, questions)
    return render(request,'index.html', {
        'questions': page_obj,
        'page_obj': page_obj,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
    })


def hot(request):
    questions = Question.objects.best_questions()
    page_obj = paginate(request, questions)
    return render(request,'hot.html', {
        'questions':page_obj,
        'page_obj': page_obj,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
    })


@login_required
def ask(request):
    if request.method == 'GET':
        form = AskForm()
    else:
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user.profile
            question.save()
            return redirect(reverse('question', kwargs={'pk': question.pk}))
    ctx = {
        'form': form,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best()
    }
    return render(request, 'ask.html', ctx)


def login(request):
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect("/") # нужны правильные редиректы!

    ctx = {
        'form': form,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best()
    }
    return render(request, 'login.html', ctx)


def logout(request):
    auth.logout(request)
    return redirect("/")


def question(request, pk):
    question = Question.objects.question_by_pk(pk)
    this_answers = Answer.objects.get_by_question(question)
    page_obj = paginate(request, this_answers, 3)
    return render(request, 'question.html', {
        'question': question,
        'answers': page_obj,
        'page_obj': page_obj,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
    })


def settings(request):
    return render(request, 'settings.html', {
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
    })


def signup(request):
    return render(request, 'signup.html', {
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
    })


def tag(request, tagname):
    questions = Question.objects.question_by_tag(tagname)
    page_obj = paginate(request, questions)
    return render(request, 'tag.html', {
        'questions':page_obj,
        'page_obj': page_obj,
        'tagname': tagname,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
    })
