from django import forms
from app.models import Question


class LoginForm(forms.Form):
    # required=True - обязательное ли поле
    # cleaned_data - поля с которыми можно работать, их получилось получить
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
