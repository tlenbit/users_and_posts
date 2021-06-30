import random
import string


class Settings:
    USERS_COUNT = 10
    MAX_POSTS_COUNT = 10
    LIKES_COUNT = 10

    BASE_URL = 'http://127.0.0.1:8000/api/'
    CREATE_USER_URL = BASE_URL + 'users/register/'
    CREATE_POST_URL = BASE_URL + 'posts/'
    CREATE_LIKE_URL = BASE_URL + 'likes/'
    GET_TOKEN_URL = BASE_URL + 'token/'

    RANDOM_STRING_LENGTH = 10
    REQUEST_TIMEOUT = 10  # in seconds


def populate(objects, field, values):
    for obj, value in zip(objects, values):
        setattr(obj, field, value)


def is_populated(objects, field):
    return all((getattr(obj, field) for obj in objects))


def generate_str():
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(Settings.RANDOM_STRING_LENGTH))


def generate_email():
    return f'{generate_str()}@gmail.com'
