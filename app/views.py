from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def rightbar(request):
    return {
        'say': "dssd"
    }

best_rightbar = {
    'tags': [{
        'pop': 1,
        'tag_name': 'MySQL'
    }, {
        'pop': 2,
        'tag_name': 'Perl'
    }, {
        'pop': 3,
        'tag_name': 'Python'
    }, {
        'pop': 3,
        'tag_name': 'TechnoPark'
    }, {
        'pop': 1,
        'tag_name': 'DJango'
    }, {
        'pop': 2,
        'tag_name': 'Mail'
    }, {
        'pop': 1,
        'tag_name': 'FireFox'
    }],
    'users': ['Ivan Gorshkov', 'Oleg Urgens', 'Fedor Surovcev', 'Prohor Surovcev', 'Ivan Hilko'],
}

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
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)

    return render(request, 'index.html', {
        'questions': paginator,
        'paginator': paginator,
        **best_rightbar
    })


def settings(request):
    return render(request, 'settings.html', {})


def tag(request, tag):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)
    return render(request, 'tag.html', {
        'tag': tag,
        'questions': paginator,
        'paginator': paginator,
        **best_rightbar
    })


def question(request, id):
    paginator = Paginator(questions[id]['answers'], 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)
    return render(request, 'answer.html', {
        'id': id,
        'one_question': questions[id],
        'answers': paginator,
        'paginator': paginator,
        **best_rightbar
    })


def login(request):
    return render(request, 'login.html', {
        **best_rightbar
    })


def settings(request):
    return render(request, 'settings.html', {
        **best_rightbar
    })


def register(request):
    return render(request, 'register.html', {
        **best_rightbar
    })


def ask(request):
    return render(request, 'question.html', {
        **best_rightbar
    })


def hot(request):
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    paginator = paginator.get_page(page)

    return render(request, 'hot.html', {
        'questions': paginator,
        'paginator': paginator,
        **best_rightbar
    })
