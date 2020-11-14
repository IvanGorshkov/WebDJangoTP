from django.core.management.base import BaseCommand
from app.models import Questions, Answers, Tags, Users, QuestionsLikes, AnswersLikes
from django.contrib.auth.models import User
from random import randint, choice, choices
from faker import Faker

f = Faker()

small = [100, 200, 4000, 10000, 3000, 10000]
medium = [1000, 2000, 40000, 100000, 30000, 100000]
large = [10000, 10000, 100000, 1000000, 1000000, 1000000]


class Command(BaseCommand):
    help = 'Generate the database with some values'

    def add_arguments(self, parser):
        parser.add_argument('--db_size', type=str, help="DB size: small, medium, large")
        parser.add_argument('--users', type=int, help='Users count')
        parser.add_argument('--tags', type=int, help='Tags count')
        parser.add_argument('--questions', type=int, help='Questions count')
        parser.add_argument('--answers', type=int, help='Answers count')
        parser.add_argument('--likes_questions', type=int, help='Questions likes count')
        parser.add_argument('--likes_answers', type=int, help='Answers likes count')

    def generate_users(self, cnt):
        if cnt is None:
            return False

        print('Generate {} users'.format(cnt))

        users = [
            User(username=f.first_name() + str(i), email=f.email())
            for i in range(cnt)
        ]
        User.objects.bulk_create(users, cnt)

        objs = [
            Users(
                user=User.objects.get(pk=i),
                nick=User.objects.get(pk=i).username
            ) for i in range(1, cnt + 1)
        ]

        Users.objects.bulk_create(objs, cnt)

    def generate_tags(self, cnt):
        if cnt is None:
            return False

        print('Generate {} tags'.format(cnt))

        tags = [
            Tags(
                title=f.word() + str(i)
            ) for i in range(cnt)
        ]

        Tags.objects.bulk_create(tags, cnt)

    def generate_questions(self, cnt):
        if cnt is None:
            return False

        print('Generate {} questions'.format(cnt))
        author_ids = list(Users.objects.all())
        tags_ids = list(Tags.objects.all())
        questions = [
            Questions(
                title=f.sentence(nb_words=10),
                text=f.paragraph(nb_sentences=5),
                date=f.date_this_year(),
                likes=f.pyint(0, 1000),
                views=f.pyint(0, 10000),
                author=choice(author_ids)
            ) for i in range(cnt)
        ]

        Questions.objects.bulk_create(questions, cnt)

        for item in Questions.objects.all():
            for i in set(choices(tags_ids, k=randint(1, 7))):
                item.tags.add(i)
            item.save()

    def generate_answers(self, cnt):
        if cnt is None:
            return False

        print('Generate {} answers'.format(cnt))
        author_ids = list(Users.objects.all())
        question_ids = list(Questions.objects.all())
        answers = [
            Answers(
                text=f.paragraph(nb_sentences=10),
                correct=choice([True, False]),
                author=choice(author_ids),
                date=f.date_this_year(),
                likes=f.pyint(0, 1000),
                question=choice(question_ids)
            ) for _ in range(cnt)
        ]

        Answers.objects.bulk_create(answers, cnt)

    def generate_likes_questions(self, cnt):
        if cnt is None:
            return
        print('Generate {} likes_questions'.format(cnt))
        author_ids = list(Users.objects.all())
        question_ids = list(Questions.objects.all())
        likes = [
            QuestionsLikes(
                question=choice(question_ids),
                author=choice(author_ids),
                status=choice([True, False]),
            ) for _ in range(cnt)
        ]
        QuestionsLikes.objects.bulk_create(likes, cnt)

    def generate_likes_answers(self, cnt):
        if cnt is None:
            return
        print('Generate {} likes_answers'.format(cnt))
        author_ids = list(Users.objects.all())
        answers_ids = list(Answers.objects.all())
        likes = [
            AnswersLikes(
                answer=choice(answers_ids),
                author=choice(author_ids),
                status=choice([True, False]),
            ) for _ in range(cnt)
        ]
        AnswersLikes.objects.bulk_create(likes, cnt)

    def handle(self, *args, **options):
        users_count = options.get('users')
        tags_count = options.get('tags')
        questions_count = options.get('questions')
        answers_count = options.get('answers')
        like_questions_count = options.get('likes_questions')
        like_answers_count = options.get('likes_answers')

        if options.get('db_size') == 'small':
            users_count = small[0]
            tags_count = small[1]
            questions_count = small[2]
            answers_count = small[3]
            like_questions_count = small[4]
            like_answers_count = small[5]
        elif options.get('db_size') == 'medium':
            users_count = medium[0]
            tags_count = medium[1]
            questions_count = medium[2]
            answers_count = medium[3]
            like_questions_count = medium[4]
            like_answers_count = medium[5]
        elif options.get('db_size') == 'large':
            users_count = large[0]
            tags_count = large[1]
            questions_count = large[2]
            answers_count = large[3]
            like_questions_count = large[4]
            like_answers_count = large[5]
        self.generate_users(users_count)
        self.generate_tags(tags_count)
        self.generate_questions(questions_count)
        self.generate_answers(answers_count)
        self.generate_likes_questions(like_questions_count)
        self.generate_likes_answers(like_answers_count)
