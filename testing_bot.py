import asyncio
import aiohttp
import string
import random
from dataclasses import dataclass
import async_timeout
from rest_framework import status



USERS_COUNT = 100
CREATE_USER_URL = 'http://127.0.0.1:8000/api/users/'
RANDOM_STRING_LENGTH = 10
REQUEST_TIMEOUT = 100  # in seconds


@dataclass
class User:
    username: str
    email: str
    password: str

    def to_json(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }


async def post_user(session, url, user):
    with async_timeout.timeout(REQUEST_TIMEOUT):
        async with session.post(url, data=user.to_json()) as response:
            return response


def generate_users():
    return [
        User(username=generate_str(),
             password=generate_str(),
             email=generate_email())
        for _ in range(USERS_COUNT)
    ]


def generate_str():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(RANDOM_STRING_LENGTH))


def generate_email():
    return f'{generate_str()}@gmail.com'


async def test_users_creation():
    async with aiohttp.ClientSession() as session:
        users = generate_users()
        post_user_coroutines = [post_user(session, CREATE_USER_URL, user) for user in users]
        responses = await asyncio.gather(*post_user_coroutines)

        for response in responses:
            assert response.status == status.HTTP_201_CREATED


async def main():
    await test_users_creation()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
