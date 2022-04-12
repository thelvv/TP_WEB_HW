from django.core.management.base import BaseCommand
from random import choice, randint
from faker import Faker

from app.models import Question
from app.models import Answer
from app.models import User
from app.models import Author
from app.models import Tag

fake = Faker()


def fill_users(num):
    users = list(
        User.objects.values_list(
            'identificator', flat=True
        )
    )
    users_count = User.objects.all().count()
    for i in range(1, num):
        author = Author.objects.create()
        User.objects.create(
            identificator=users_count + i + 1,
            name=fake.name(),
            password='1234',
            email=fake.email(),
            author=author
        )


def fill_questions(num):
    users_ids = list(
        User.objects.values_list(
            'id', flat=True
        )
    )
    tags = Tag.objects.all()
    count = len(Question.objects.all())
    for i in range(1, num):
        question = Question.objects.create(
            identificator=count + i,
            rating=randint(0, int(num/2)),
            answers_count=0,
            title=fake.sentence()[:128],
            text='. '.join(fake.sentences(fake.random_int(min=2, max=5))),
            user=User.objects.filter(id=choice(users_ids)).first(),
        )
        question.tags.add(choice(tags))


def fill_answers(num):
    questions_ids = list(
        Question.objects.values_list(
            'identificator', flat=True
        )
    )
    users_ids = list(
        User.objects.values_list(
            'identificator', flat=True
        )
    )

    for i in range(1, num):
        question_ = Question.objects.filter(identificator=choice(questions_ids)).first()
        question_.answers_count += 1
        question_.save(update_fields=['answers_count'])
        Answer.objects.create(
            author=User.objects.filter(identificator=choice(users_ids)).first(),
            question=question_,
            rating=randint(0, int(num/3)),
            text='. '.join(fake.sentences(fake.random_int(min=2, max=5))),
        )


def fill_tags(cnt):
    for i in range(cnt):
        Tag.objects.create(
            title=fake.word(),
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        if options['all']:
            n = options['all']
            print("Generating the base")
            fill_tags(n * 5)
            fill_users(n * 100)
            fill_questions(n * 100)
            fill_answers(n * 100)
            print("done!")

        if options['users']:
            print("Generating ", options['users'], " users")
            fill_users(options['users'])

        if options['questions']:
            print("Generating ", options['questions'], " questions")
            fill_questions(options['questions'])

        if options['answers']:
            print("Generating ", options['answers'], " answers")
            fill_answers(options['answers'])

        if options['tags']:
            print("Generating ", options['tags'], " tags")
            fill_answers(options['tags'])

    def add_arguments(self, parser):
        parser.add_argument('--all', type=int)
        parser.add_argument('--questions', type=int)
        parser.add_argument('--answers', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
