"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('tag/<slug:id_tag>/', views.tag, name='tag'),
    path('question/<int:id>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('register/', views.register, name='register'),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot'),
    path('vote/', views.vote, name='vote'),
    path('vote_answer/', views.vote_answer, name='vote_answer'),
    path('correct/', views.correct, name='correct')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'app.views.error_404_view'
handler500 = 'app.views.error_500_view'
