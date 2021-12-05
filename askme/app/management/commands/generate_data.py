from django.core.management.base import BaseCommand, CommandError
from app.models import Profile, Question, Tag, Answer, LikeAnswer, LikeQuestion
from django.contrib.auth.models import User
from random import choice
from faker import Faker
from django.db import IntegrityError

f = Faker()

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            '--db_size',
            choices=['small', 'medium', 'large'],
            help='choose how many data to fill the database'
        )
        parser.add_argument('--add_users', type=int, help='users creation')
        parser.add_argument('--add_tags', type=int, help='tags creation')
        parser.add_argument('--add_questions', type=int, help='questions creation')
        parser.add_argument('--add_answers', type=int, help='answers creation')
        parser.add_argument('--add_likes', type=int, help='likes creation')


    def handle(self, *args, **options):
        opt = options['db_size']
        if (opt):
            percent = {
                'small': 0.0005,
                'medium': 0.001,
                'large': 0.005,
                }.get(opt, 0.00005)
                # self.stdout.write(percent)
            self.bd_generate(percent)

        if (options['add_users']):
            self.generate_users(options['add_users'])
        if (options['add_tags']):
            self.generate_tags(options['add_tags'])
        if (options['add_questions']):
            self.generate_questions(options['add_questions'])
        if (options['add_answers']):
            self.generate_answers(options['add_answers'])
        if (options['add_likes']):
            self.generate_likes(options['add_likes'])



    def bd_generate(self, percen):
        MAX_USER = 10000
        MAX_QUESTION = 100000
        MAX_TAG = 10000
        MAX_ANSWER = 1000000
        MAX_LIKE = 2000000

        if (percen > 1):
            return;

        self.generate_users(int(percen * MAX_USER))
        self.generate_tags(int(percen * MAX_TAG))
        self.generate_questions(int(percen * MAX_QUESTION))
        self.generate_answers(int(percen * MAX_ANSWER))
        self.generate_likes(int(percen * MAX_LIKE))

    def generate_users(self, cnt):
        for i in range(cnt):
            name = f.first_name()
            user = User(username=name, email=f.email(), first_name=name)
            user.set_password('xxx')

            try:
                user.save()
            except IntegrityError:
                continue

            profile = Profile()
            profile.user = user
            num_ava = f.random_int(min=21, max=25)
            profile.avatar = f'../static/test_image/test{num_ava}.jpg'
            profile.save()

    def generate_tags(self, cnt):
        for i in range(cnt):
            tag = Tag()
            tag.name = f.word()
            tag.save()

    def generate_answers(self, cnt):
        for i in range(cnt):
            answer = Answer()
            answer.is_correct = choice([True, False])
            answer.text = ' '.join(f.sentences(f.random_int(min=3, max=6)))
            answer.question_id = self.get_random_question_id()
            answer.user_id = self.get_random_user_id()

            answer.save()

    def get_random_question_id(self):
        questions_id = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        return choice(questions_id)

    def get_random_user_id(self):
        user_id = list(
            User.objects.values_list(
                'id', flat=True
            )
        )
        return choice(user_id)

    def get_random_answer_id(self):
        answer_id = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        return choice(answer_id)

    def get_random_tag_id(self):
        tag_id = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        return choice(tag_id)

    def generate_likes(self, cnt):
        for i in range(cnt):
            like_answer = LikeAnswer()
            like_question = LikeQuestion()

            qst = Question.objects.get(id = self.get_random_question_id())
            like_question.question_id = qst.id

            like_answer.answer_id = self.get_random_answer_id()

            if (f.random_int(min=1, max=10) < 4):
                like_answer.is_like = False
                like_question.is_like = False
                qst.rating -= 1
            else:
                like_answer.is_like = True
                like_question.is_like = True
                qst.rating += 1

            like_question.user_id = self.get_random_user_id()
            like_answer.user_id = self.get_random_user_id()

            try:
                like_answer.save()
                like_question.save()
                qst.save()

            except IntegrityError:
                continue


    def generate_questions(self, cnt):
        for i in range(cnt):
            question = Question()
            question.title = f.sentence()[:128]
            question.text = ' '.join(f.sentences(f.random_int(min=5, max=8)))
            question.user_id = self.get_random_user_id()

            question.save()
            for i in range(f.random_int(min=1, max=3)):
                question.tags.add(self.get_random_tag_id())
