from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from app.models import Questions, Answers, User, Users, Tags
from app.forms import LoginForm, RegisterForm, AskForm, SettingsForm, AnswerForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def paginator(data, request, pages=5):
    obj_paginator = Paginator(data, pages)
    page = request.GET.get('page')
    obj_paginator = obj_paginator.get_page(page)
    return obj_paginator


def index(request):
    data = paginator(Questions.objects.new(), request)
    return render(request, 'index.html', {
        'data': data,
    })


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    data = paginator(Questions.objects.tag(tag), request)
    return render(request, 'tag.html', {
        'tag': tag,
        'data': data
    })


def error_404_view(request, exception):
    return render(request, '404.html')


def error_500_view(request):
    return render(request, '404.html')


def question(request, id):
    if request.method == "GET":
        form = AnswerForm(initial={
            'id': id,
        })
    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = form.cleaned_data['id']
            answer.author_id = request.user.pk
            answer.save()

    data = paginator(Answers.objects.answers_by_question(id), request)
    return render(request, 'answer.html', {
        'id': id,
        'one_question': Questions.objects.one_question(id),
        'data': data,
        'form': form
    })


def login(request):
    if request.method == "GET":
        form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get("next", "/"))

    ctx = {'form': form}
    return render(request, 'login.html', ctx)


@login_required
def settings(request):
    if request.method == "GET":
        form = SettingsForm()
    if request.method == "POST":
        form = SettingsForm(data=request.POST)
    ctx = {'form': form}
    return render(request, 'settings.html', ctx)


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    if request.method == "GET":
        form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=True)
            if form.cleaned_data['avatar'] is None:
                author = Users(user_id=user.pk, nick=form.cleaned_data['username'])
            else:
                author = Users(user_id=user.pk, nick=form.cleaned_data['username'], avatar=form.cleaned_data['avatar'])
            author.save()
            print(form.cleaned_data['avatar'])
            auth.login(request, user)
            return redirect(request.GET.get("next", "/"))

    ctx = {'form': form}
    return render(request, 'register.html', ctx)


@login_required
def ask(request):
    if request.method == "GET":
        form = AskForm()
    if request.method == "POST":
        form = AskForm(data=request.POST)
        if form.is_valid():
            print(request.user.pk)
            ask_question = form.save(commit=False)
            ask_question.author = Users.objects.get(user=request.user.pk)
            ask_question.save()
            tags = form.cleaned_data['tags'].split(' ')
            for one_tag in tags:
                create = Tags.objects.create(title=one_tag)
                create.save()
                ask_question.tags.add(create)

            return redirect(reverse('question', kwargs={'id': ask_question.pk}))
    ctx = {'form': form}
    return render(request, 'question.html', ctx)


def hot(request):
    data = paginator(Questions.objects.hot(), request)
    return render(request, 'hot.html', {
        'data': data,
    })
