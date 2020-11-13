from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Questions, Answers

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'pic': 'img/180.png',
        'text': """Guys, i have trapbles with a moon park! Please help me Guys, i have trapbles with a moon park! 
                    Please help me Guys, i have trapbles with a moon park! Please help meGuys, i
                    have trapbles with a moon park! Please help me Guys, i have trapbles with 
                    a moon park! Please help me""",
        'date': '23.12.2020',
        'like': 234,
        'dislike': 23,
        'tag': ["black-jack", "bender", "bender"],
        'answers': [{
            'id': idy,
            'pic': 'img/180.png',
            'likes': 12,
            'dislike': 13,
            'text': """%d Gueffs with a moon park! Please help meGues with a moon park! Please 
                        help meGues with a moon park! Please help meGues with a moon park! Please help 
                        meGues with a moon park! Please help me""" % idy,
            'date': '12.10.2020'
        } for idy in range(100)]
    } for idx in range(10)
]

def index(request):
    paginator = Paginator(Questions.objects.new(), 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)

    return render(request, 'index.html', {
        'questions': paginator,
        'paginator': paginator,
    })


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    paginator = Paginator(Questions.objects.tag(tag), 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)
    return render(request, 'tag.html', {
        'tag': tag,
        'questions': paginator,
        'paginator': paginator,
    })


def question(request, id):
    paginator = Paginator(Answers.objects.answers_by_question(id), 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)
    return render(request, 'answer.html', {
        'id': id,
        'one_question': Questions.objects.one_question(id),
        'answers': paginator,
        'paginator': paginator,
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
    paginator = Paginator(Questions.objects.hot(), 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)

    return render(request, 'hot.html', {
        'questions': paginator,
        'paginator': paginator,
    })
