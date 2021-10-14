from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from app.models import Profile, Question, Answer, Tag, LikeAnswer, LikeQuestion
import itertools
from django.contrib import auth
from app.forms import *
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import IntegrityError

# для realtime
import jwt
from django.conf import settings

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
        # 'likes': LikeQuestion.objects.likes_user(request.user)
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
        form = AskForm(data=request.POST, user=request.user)
        if form.is_valid():
            question = form.save()
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
        form = AnswerForm(data=request.POST, user=request.user, question_pk=pk)
        if(request.user.is_authenticated == False):
            return redirect(f'/login/?next=/question/{pk}/')
        if form.is_valid():
            answer = form.save()
            return redirect(reverse('question', kwargs={'pk': pk}))

    question = Question.objects.question_by_pk(pk)
    this_answers = Answer.objects.get_by_question(question)
    page_obj = paginate(request, this_answers, 3)

    # realtime
    channel_id = str(pk)
    token = jwt.encode({"sub": channel_id}, '4bc52a37-ebc9-4d64-a1dd-84dc5fc9f8a7')

    ctx = {
        'form': form,
        'question': question,
        'answers': page_obj,
        'page_obj': page_obj,
        'tags': Tag.objects.get_best(),
        'members': Profile.objects.get_best(),
        'token': token,
        'quest_id': pk,
    }
    is_author = False
    if request.user.is_authenticated == True:
        if question.user == request.user:
            is_author = True

    ctx['is_author'] = is_author
    return render(request, 'question.html', ctx)


@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'avatar': request.user.profile.avatar,
        })
    else:
        form = SettingsForm(
            data=request.POST, files=request.FILES,
            instance=request.user.profile)

        if form.is_valid():
            profile = request.user.profile
            request.user.profile.delete()
            profile = Profile(
                user = request.user,
                avatar=request.FILES.get('avatar', request.user.profile.avatar),
                birthday = profile.birthday
            )

            profile.save()


            request.user.username = request.POST['username']
            request.user.email = request.POST['email']
            request.user.first_name = request.POST['first_name']
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
            user = User.objects.create_user(
                username = form.cleaned_data.get('username'),
                first_name = form.cleaned_data.get('first_name'),
                email = form.cleaned_data.get('email'),
                password = form.cleaned_data.get('password'))
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


@require_POST
@login_required
def vote(request):
    data = request.POST
    if (data['like'] == 'question'):
        like = LikeQuestion()
        content = Question.objects.get(pk = data['id'])
        like.question = content
    elif (data['like'] == 'answer'):
        like = LikeAnswer()
        content = Answer.objects.get(pk = data['id'])
        like.answer = content

    like.user = request.user
    if data['action'] == 'like':
        like.is_like = True
    else:
        like.is_like = False

    try:
        like.save()
    except IntegrityError:
        return JsonResponse({ 'error': 'IntegrityError' })

    return JsonResponse({ 'likes': content.like() })


@require_POST
@login_required
def correct(request):
    data = request.POST
    question = Question.objects.get(pk = data['qid'])
    if question.user == request.user:
        answer = Answer.objects.get(pk = data['aid'])
        answer.is_correct = not answer.is_correct

        answer.save()

        return JsonResponse({ 'is_correct': answer.is_correct })

    return JsonResponse({ 'error': 'not_author' })
