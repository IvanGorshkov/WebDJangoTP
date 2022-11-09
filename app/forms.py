from django import forms
from django.contrib.auth.models import User
from app.models import Questions, Answers
from django.contrib.auth.forms import UserCreationForm
from string import Template
from django.utils.safestring import mark_safe


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


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html = Template("""<br/><br/><img id = "myimage" src="$link" width="100" height="100"/>""")
        return mark_safe(html.substitute(link=value[8:]))


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=PictureWidget)
    change = forms.ImageField(required=False)
    change.widget.attrs['onchange'] = 'readURL(this)'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'change']


class AnswerForm(forms.ModelForm):
    id_question = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Answers
        fields = ['text', 'id_question']
