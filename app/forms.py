from django import forms
from django.contrib.auth.models import User
from app.models import Questions, Answers
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    class Meta:
        model = Questions
        fields = ["title", "text", "tags"]


class RegisterForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'avatar']


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']


class AnswerForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Answers
        fields = ['text', 'id']
