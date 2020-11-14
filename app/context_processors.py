from app.models import Users
from app.models import Tags

def rightbar(request):
    return {
        'tags': Tags.objects.popular_tags(),
        'users': Users.objects.popular_users(),
    }