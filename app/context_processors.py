from app.models import Users
from app.models import Tags


def rightbar(request):
    if request.session.session_key is not None and request.user.is_superuser is not True:
        avatar = Users.objects.get_avatar(request.user.pk)
    else:
        avatar = ""
        print(avatar)
    return {
        'tags': Tags.objects.popular_tags(),
        'users': Users.objects.popular_users(),
        'avatar': avatar,
    }