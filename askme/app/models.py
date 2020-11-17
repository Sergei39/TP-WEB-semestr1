from django.db import models

# Create your models here.

# modelMeneger - класс в котором пишется логика проекта
class QuestionManager(models.Manager):
    def last_questions(self):
        return self.order_by('-data_create')

    def best_questions(self):
        return self.filter()

    def question_by_pk(self, pk):
        return self.get(pk = pk)

    def question_by_tag(self, tag):
        return self.filter(tags__name = tag)


class User(models.Model):
    # информация о пароле, логине пользователя

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    nick_name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    avatar = models.ImageField(upload_to='static/madia/image/avatar/',
                                default = 'static/media/image/avatar/200.jpeg',
                                blank = True,
                                verbose_name='Аватарка')

    # чтобы сразу принтить (когда принтиться автор, принтиться определенные поля)
    def __str__(self):
        return self.nick_name

    # user = models.OneToOneField(
    #     'User',
    #     on_delete=models.CASCADE,
    #     related_name='profile'
    # )

    # содержится информация, как класс должен создаваться
    # джанго - админка
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Question(models.Model):
    # verbose_name - указание что содерижтся в переменной (правило хорошего тона)
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # автоматически добавляет дату создания

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def like(self):
        like = Owner.objects.filter(question = self, like__is_like = True).count()
        dislike = Owner.objects.filter(question = self, like__is_like = False).count()
        return like - dislike

    def answer(self):
        return Answer.objects.filter(question = self).count()

    # связь многие ко многим, создает отдельную табличку с тремя полями (синтетический id, ключ автора, ключ статьи)

    # связь сущностей (один ко многим)
    # на уровне бд, в таблице Article создатся поле authorId (id, которым можно сослаться на автора)
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey('Profile', default='', on_delete=models.SET_DEFAULT, blank=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerManager(models.Manager):
    def get_by_question(self, question_obj):
        return self.filter(question = question_obj.pk)


class Answer(models.Model):
    is_correct = models.BooleanField(default=False, verbose_name='Корректный')
    text = models.TextField(verbose_name='Текст')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = AnswerManager()

    def __str__(self):
        return self.text

    def like(self):
        like = Owner.objects.filter(answer = self, like__is_like = True).count()
        dislike = Owner.objects.filter(answer = self, like__is_like = False).count()
        return like - dislike

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TagManager(models.Manager):
    def get_best(self):
        return self.all()[:10]
    def get_all(self):
        return self.all()


class Tag(models.Model):
    name = models.CharField(max_length=1024, verbose_name='Название')
    data_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    objects = TagManager()

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
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    content = models.OneToOneField('Owner', on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
