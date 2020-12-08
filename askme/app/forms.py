from django import forms
from app.models import Question, Profile, Answer, Tag
from django.contrib.auth.models import User
import re


class LoginForm(forms.Form):
    # required=True - обязательное ли поле
    # cleaned_data - поля с которыми можно работать, их получилось получить
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']

    def add_tags(self, question):
        tags = self.cleaned_data['tags']
        tags = re.sub(r'[.,]', ' ', tags).split()
        for tag in tags:
            tag_model = Tag.objects.get_tag(tag)
            if tag_model is None:
                tag_model = Tag.objects.create(name = tag)
            question.tags.add(tag_model)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.CharField()

    def save(self, commit=True):
        question = super().save(commit=False)
        question.user = self.user
        if commit==True:
            question.save()
            self.add_tags(question)
        return question;


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question_pk = kwargs.pop('question_pk', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.user = self.user
        answer.question = Question.objects.get(pk = self.question_pk)
        if commit == True:
            answer.save()
        return answer;


class RegistrForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

    password = forms.CharField()
    repeat_password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['repeat_password'].widget = forms.PasswordInput()


    def clean(self):
        cleaned_data = super(RegistrForm, self).clean()
        psw = cleaned_data.get('password')
        repeat_psw = cleaned_data.get('repeat_password')

        if repeat_psw != psw:
            msg = "Passwords do not match"
            self.add_error('password', msg)
            self.add_error('repeat_password', msg)



class SettingsForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()

    class Meta:
        model = Profile
        fields = ["avatar"]
