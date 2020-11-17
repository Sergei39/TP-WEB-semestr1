from django.core.management.base import BaseCommand, CommandError
from app.models import Profile, Question, Tag, Answer, Like, Owner
from random import choice
from faker import Faker

f = Faker()

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('poll_ids', type=int)

    def handle(self, *args, **options):
        a = options['poll_ids']
        self.stdout.write('hello')
        self.bd_generate(0.0005)


    def bd_generate(self, percen):
        MAX_USER = 10000
        MAX_QUESTION = 10000
        MAX_TAG = 10000
        MAX_ANSWER = 100000
        MAX_LIKE = 200000

        if (percen > 1):
            return;

        for i in range(int(percen * MAX_USER)):
            self.generate_user()
        for i in range(int(percen * MAX_TAG)):
            self.generate_tag()
        for i in range(int(percen * MAX_QUESTION)):
            self.generate_question()
        for i in range(int(percen * MAX_ANSWER)):
            self.generate_answer()
        for i in range(int(percen * MAX_LIKE)):
            self.generate_like()

    def generate_user(self):
        user = Profile()
        user.nick_name = f.first_name()
        user.save()

    def generate_tag(self):
        tag = Tag()
        tag.name = f.word()
        tag.save()

    def generate_answer(self):
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
            Profile.objects.values_list(
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

    def generate_like(self):
        owner = Owner()
        if (choice([True, False])):
            question_id = self.get_random_question_id()
        else:
            answer_id = self.get_random_answer_id()
        owner.save()


        like = Like()
        like.is_like = choice([True, False])
        like.content = owner
        like.user_id = self.get_random_user_id()

        like.save()


    def generate_question(self):
        question = Question()
        question.title = f.sentence()[:128]
        question.text = ' '.join(f.sentences(f.random_int(min=3, max=6)))
        question.user_id = self.get_random_user_id()

        question.save()
        for i in range(f.random_int(min=1, max=3)):
            question.tags.add(self.get_random_tag_id())
