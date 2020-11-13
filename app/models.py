from django.db import models
from django.db.models import Count

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-date')

    def hot(self):
        return self.order_by('-views')

    def tag(self, selected_tag):
        return self.filter(tags__title=selected_tag).order_by('-date')

    def one_question(self, id):
        return self.filter(pk=id).first()


class Questions(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Вопрос")
    tags = models.ManyToManyField('Tags')
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    objects = QuestionManager()

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
    text = models.TextField(verbose_name="Отыет")
    correct = models.BooleanField(verbose_name="Правильность")
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    objects = AnswerManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Tags(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Тег')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class UsersManager(models.Manager):
    def popular_users(self):
        query_result = Answers.objects.values('author__id').annotate(disease_count=Count('author__id')).order_by('-disease_count')
        return query_result.values('author__id').values('author__nick')[:3]


class Users(models.Model):
    login = models.CharField(max_length=100, verbose_name='Логин')
    email = models.EmailField(max_length=100, verbose_name='Почта')
    nick = models.CharField(max_length=100, verbose_name='Логин')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    avatar = models.ImageField(max_length=1024, verbose_name='Аватар')
    objects = UsersManager()

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class QuestionsLikes(models.Model):
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    status = models.BooleanField(null=True, verbose_name='Отметка')

    def __str__(self):
        return "Лайк вопроса {}".format(self.question.title)

    class Meta:
        verbose_name = 'Лайки вопроса'
        verbose_name_plural = 'Лайки вопросов'


class AnswersLikes(models.Model):
    author = models.ForeignKey('Users', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answers', on_delete=models.CASCADE)
    status = models.BooleanField(null=True, verbose_name='Отметка')

    def __str__(self):
        return "Лайк ответа {}".format(self.answer.question.title)

    class Meta:
        verbose_name = 'Лайки ответа'
        verbose_name_plural = 'Лайки ответов'
