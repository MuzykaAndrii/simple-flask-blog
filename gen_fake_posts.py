from app import db
from app.models import Post
from faker import Faker
from random import randint

fake = Faker()

def gen(count_of_posts, user_start, user_end):
    for _ in range(0, count_of_posts):
        post = Post(fake.sentence(nb_words=3), fake.paragraph(nb_sentences=50), randint(user_start, user_end))
        post.save()
    return '{} posts are generated'.format(count_of_posts)