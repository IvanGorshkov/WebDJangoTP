from django.contrib import admin
from app import models

admin.site.register(models.Answers)
admin.site.register(models.Questions)
admin.site.register(models.QuestionsLikes)
admin.site.register(models.AnswersLikes)
admin.site.register(models.Tags)
admin.site.register(models.Users)
# Register your models here.
