from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from app.models import Profile, Question, Answer, Tag, LikeAnswer, LikeQuestion
import itertools
from django.contrib import auth
from app.forms import *
from django.contrib.auth.models import User
import re



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
            tags = form.cleaned_data['tags']
            tags = re.sub(r'[.,]', ' ', tags).split()
            for tag in tags:
                tag_model = Tag.objects.get_tag(tag)
                if tag_model is None:
                    tag_model = Tag.objects.create(name = tag)
                question.tags.add(tag_model)
            return redirect(reverse('question', kwargs={'pk': question.pk}))
    ctx = {
        'form': form,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best()
    }
    return render(request, 'ask.html', ctx)


def login(request):
    error = None
    if request.method == 'GET':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                error = 'Incorrect login or password'

    ctx = {
        'form': form,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
        'continue': request.GET.get('next', '/'),
        'error': error,
    }
    return render(request, 'login.html', ctx)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next', '/'))


def question(request, pk):
    if request.method == 'GET':
        form = AnswerForm()
    else:
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user.profile
            answer.question = Question.objects.get(pk = pk)
            answer.save()
            return redirect(reverse('question', kwargs={'pk': pk}))

    question = Question.objects.question_by_pk(pk)
    this_answers = Answer.objects.get_by_question(question)
    page_obj = paginate(request, this_answers, 3)
    return render(request, 'question.html', {
        'form': form,
        'question': question,
        'answers': page_obj,
        'page_obj': page_obj,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
    })


@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'avatar': request.user.profile.avatar
        })
    else:
        form = SettingsForm(data=request.POST)
        if form.is_valid():
            request.user.username = form.username
            request.user.email = form.email
            request.user.first_name = form.first_name
            request.user.profile.avatar = form.avatar
            request.user.save()

            return redirect('/settings/')

    ctx = {
        'form': form,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
        'continue': request.GET.get('next', '/'),
    }
    return render(request, 'settings.html', ctx)


def signup(request):
    if request.method == 'GET':
        form = RegistrForm()
    else:
        form = RegistrForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            profile = Profile(user=user)
            profile.save()
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('next', '/'))

    ctx = {
        'form': form,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
        'continue': request.GET.get('next', '/'),
    }
    return render(request, 'signup.html', ctx)


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
