from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Questions, Answers


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
    data = paginator(Answers.objects.answers_by_question(id), request)
    return render(request, 'answer.html', {
        'id': id,
        'one_question': Questions.objects.one_question(id),
        'data': data,
    })


def login(request):
    return render(request, 'login.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def register(request):
    return render(request, 'register.html', {})


def ask(request):
    return render(request, 'question.html', {})


def hot(request):
    data = paginator(Questions.objects.hot(), request)
    return render(request, 'hot.html', {
        'data': data,
    })
