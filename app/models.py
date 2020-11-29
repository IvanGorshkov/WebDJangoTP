from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-pk')

    def hot(self):
        return self.order_by('-rating')

    def tag(self, selected_tag):
        return self.filter(tags__title=selected_tag).order_by('-date')

    def one_question(self, id):
        return self.get(pk=id)


class Questions(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок', db_index=True)
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Вопрос")
    tags = models.ManyToManyField('Tags', blank=True)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    objects = QuestionManager()

    def get_avatar(self):
        return self.author.avatar.url[8:]

    def all_tags(self):
        return self.tags.all()

    def count_answers(self):
        return Answers.objects.filter(question__id=self.pk).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerManager(models.Manager):
    def answers_by_question(self, id):
        return self.filter(question_id=id)


class Answers(models.Model):
    text = models.TextField(verbose_name="Ответ")
    correct = models.BooleanField(default=False, verbose_name="Правильность")
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    objects = AnswerManager()

    def get_avatar(self):
        return self.author.avatar.url[8:]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TagsManager(models.Manager):
    def popular_tags(self):
        query_result = Questions.objects.values('tags').values('tags__title').annotate(disease_count=Count('tags__id')).order_by(
            '-disease_count')[:10]
        return query_result


class Tags(models.Model):
    title = models.CharField(unique=True, max_length=1024, verbose_name='Тег')
    objects = TagsManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class UsersManager(models.Manager):
    def popular_users(self):
        query_result = Answers.objects.values('author__id').annotate(disease_count=Count('author__id')).order_by('-disease_count')
        return query_result.values('author__id').values('author__nick')[:5]

    def get_avatar(self, id):
        return Users.objects.get(user=id).avatar.url[8:]


def avatar_upload_to(instance, filename):
    return 'static/uploads/avatars/{}/{}'.format(instance.user.id, filename)


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    nick = models.CharField(max_length=100, verbose_name='Логин')
    avatar = models.ImageField(max_length=1024, upload_to=avatar_upload_to, default="static/27804.png", verbose_name='Аватар')
    objects = UsersManager()

    def __str__(self):
        return self.nick

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class QuestionsLikes(models.Model):
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    status = models.BooleanField(default=False, verbose_name='Отметка')

    def __str__(self):
        return "Лайк вопроса {}".format(self.question.title)

    class Meta:
        verbose_name = 'Лайки вопроса'
        verbose_name_plural = 'Лайки вопросов'


class AnswersLikes(models.Model):
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answers', on_delete=models.CASCADE)
    status = models.BooleanField(default=False, verbose_name='Отметка')

    def __str__(self):
        return "Лайк ответа {}".format(self.answer.question.title)

    class Meta:
        verbose_name = 'Лайки ответа'
        verbose_name_plural = 'Лайки ответов'
