from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def settings(request):
    return render(request, 'settings.html', {})

def tag(request, tag):
    return render(request, 'tag.html', {
        'tag': tag
    })

def question(request, id):
    return render(request, 'answer.html', {
        'id': id
    })

def login(request):
    return render(request, 'login.html', {})

def settings(request):
    return render(request, 'settings.html', {})


def register(request):
    return render(request, 'register.html', {})

def new_question(request):
    return render(request, 'question.html', {})

def hot(request):
    return render(request, 'hot.html', {})
