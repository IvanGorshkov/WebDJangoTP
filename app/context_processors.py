from app.models  import Users

def rightbar(request):
    return {
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
        'users': Users.objects.popular_users(),
    }