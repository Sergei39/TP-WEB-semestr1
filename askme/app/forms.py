from django import forms
from app.models import Question, Profile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    # required=True - обязательное ли поле
    # cleaned_data - поля с которыми можно работать, их получилось получить
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']


class RegistrForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()


class SettingsForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    avatar = forms.ImageField()
