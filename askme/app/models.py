from django.db import models

# Create your models here.

# modelMeneger - класс в котором пишется логика проекта
class QuestionManager(models.Manager):
    def recent_questions(self):
        return self.filter()

    @property
    def like(self):
        return 2

    @property
    def answer(self):
        return Answer.objects.filter(question = Question.objects.filter().first().id).count()


class User(models.Model):
    # информация о пароле, логине пользователя

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    nick_name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')
    # avatar = models.ImageField(verbose_name='Аватарка')

    # чтобы сразу принтить (когда принтиться автор, принтиться определенные поля)
    def __str__(self):
        return self.nick_name

    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # содержится информация, как класс должен создаваться
    # джанго - админка
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Question(models.Model):
    # verbose_name - указание что содерижтся в переменной (правило хорошего тона)
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    data_create = models.DateField(auto_now_add=True, verbose_name='Дата создания') # автоматически добавляет дату создания

    objects = QuestionManager()

    def __str__(self):
        return self.title

    # связь многие ко многим, создает отдельную табличку с тремя полями (синтетический id, ключ автора, ключ статьи)

    # связь сущностей (один ко многим)
    # на уровне бд, в таблице Article создатся поле authorId (id, которым можно сослаться на автора)
    tag = models.ManyToManyField('Tag', related_name='question')
    user = models.ForeignKey('User', default='', on_delete=models.SET_DEFAULT, blank=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    is_correct = models.BooleanField(default=False, verbose_name='Корректный')
    text = models.TextField(verbose_name='Текст')
    data_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.text

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Tag(models.Model):
    name = models.TextField(verbose_name='Название')
    data_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Owner(models.Model):
    question = models.ForeignKey('Question', null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.CASCADE)


class Like(models.Model):
    is_like = models.BooleanField(verbose_name='Лайк? (или дизлайк)')
    data_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    content = models.OneToOneField('Owner', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
