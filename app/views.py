from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from app.models import Questions, Answers, User, Users, Tags, QuestionsLikes, AnswersLikes
from app.forms import LoginForm, RegisterForm, AskForm, SettingsForm, AnswerForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q


def paginator(data, request, pages=5):
    obj_paginator = Paginator(data, pages)
    page = request.GET.get('page')
    obj_paginator = obj_paginator.get_page(page)
    return obj_paginator


def index(request):
    data = paginator(Questions.objects.new(), request)
    info = QuestionsLikes.objects.likes(data, request.user.pk)
    return render(request, 'index.html', {
        'data': data,
        'info': zip(data, info)
    })


def tag(request, tag):
    data = paginator(Questions.objects.tag(tag), request)
    info = QuestionsLikes.objects.likes(data, request.user.pk)
    print(info)
    return render(request, 'tag.html', {
        'tag': tag,
        'data': data,
        'info': zip(data, info)
    })


def error_404_view(request, exception):
    return render(request, '404.html')


def error_500_view(request):
    return render(request, '404.html')


def question(request, id):
    if request.method == "GET":
        form = AnswerForm(initial={
            'id_question': id,
        })

    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = form.cleaned_data['id_question']
            answer.author = request.user.users
            answer.save()
            return redirect(reverse('question', kwargs={'id': form.cleaned_data['id_question']}))

    data = paginator(Answers.objects.answers_by_question(id), request)
    info = QuestionsLikes.objects.likes([Questions.objects.one_question(id)], request.user.pk)[0]
    vote_answer = AnswersLikes.objects.likes(data, request.user.pk)

    return render(request, 'answer.html', {
        'id': id,
        'one_question': Questions.objects.one_question(id),
        'data': data,
        'ans_data': zip(data, vote_answer),
        'info': info,
        'form': form
    })


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "GET":
        form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get("next", "/"))
            else:
                form.add_error('password', 'invalid password or username')

    ctx = {'form': form}
    return render(request, 'login.html', ctx)


@login_required
def settings(request):
    if request.method == "GET":
        form = SettingsForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'avatar': "/static/{}".format(Users.objects.get_avatar(request.user.pk)),
            'change': "/static/{}".format(Users.objects.get_avatar(request.user.pk))
        })
    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            if form.cleaned_data['change'] is not None:
                user.users.avatar = form.cleaned_data['change']
                user.users.save()
            user.save()
            messages.success(request, 'Form submission successful')
    form.initial['avatar'] = "/static/{}".format(Users.objects.get_avatar(request.user.pk))

    print(form.initial)
    ctx = {'form': form}
    return render(request, 'settings.html', ctx)


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
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
            ask_question = form.save(commit=False)
            ask_question.author = Users.objects.get(user=request.user.pk)
            ask_question.save()
            tags = form.cleaned_data['tags'].split(' ')
            for one_tag in tags:
                customer, created = Tags.objects.get_or_create(title=one_tag)
                ask_question.tags.add(customer)

            return redirect(reverse('question', kwargs={'id': ask_question.pk}))
    ctx = {'form': form}
    return render(request, 'question.html', ctx)


def hot(request):
    data = paginator(Questions.objects.hot(), request)
    info = QuestionsLikes.objects.likes(data, request.user.pk)
    return render(request, 'hot.html', {
        'data': data,
        'info': zip(data, info)
    })


@require_POST
@login_required
def vote(request):
    data = request.POST
    like_post = Questions.objects.get(pk=data['qid'])
    try:
        res = QuestionsLikes.objects.get(Q(author_id=request.user.pk) & Q(question_id=data['qid']))
    except QuestionsLikes.DoesNotExist:
        res = None

    if res is None:
        if data['action'] == "like":
            like_post.rating += 1
            pressed = QuestionsLikes(author_id=request.user.pk, question_id=data['qid'], status=True)
        else:
            pressed = QuestionsLikes(author_id=request.user.pk, question_id=data['qid'], status=False)
            like_post.rating -= 1
        pressed.save()
        like_post.save()
    else:
        return JsonResponse({'error': "Rating already pass"})

    return JsonResponse({'qid': data['qid'], 'rating': like_post.rating})


@require_POST
@login_required
def vote_answer(request):
    data = request.POST
    like_answer = Answers.objects.get(pk=data['aid'])
    try:
        res = AnswersLikes.objects.get(Q(author_id=request.user.pk) & Q(answer_id=data['aid']))
    except AnswersLikes.DoesNotExist:
        res = None

    if res is None:
        if data['action'] == "like":
            like_answer.rating += 1
            pressed = AnswersLikes(author_id=request.user.pk, answer_id=data['aid'], status=True)
        else:
            pressed = AnswersLikes(author_id=request.user.pk, answer_id=data['aid'], status=False)
            like_answer.rating -= 1
        pressed.save()
        like_answer.save()
    else:
        return JsonResponse({'error': "Rating already pass"})

    return JsonResponse({'aid': data['aid'], 'rating': like_answer.rating})



@require_POST
@login_required
def correct(request):
    data = request.POST
    obj = Answers.objects.get(pk=data['aid'])
    obj.correct = not obj.correct
    obj.save()
    return JsonResponse({'aid': data['aid']})