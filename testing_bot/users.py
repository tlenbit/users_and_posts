import aiohttp
import async_timeout
import asyncio
import json
import pydantic

from rest_framework import status
from typing import Optional
from utils import Settings
from utils import generate_email
from utils import generate_str
from utils import is_populated
from utils import populate


class User(pydantic.BaseModel):
    username: str
    email: str
    password: str
    user_id: Optional[int]
    token: Optional[str]


async def login_user(session, user):
    with async_timeout.timeout(Settings.REQUEST_TIMEOUT):
        post_data = {
            'username': user.username,
            'password': user.password,
        }
        async with session.post(Settings.GET_TOKEN_URL, data=post_data) as response:
            assert response.status == status.HTTP_200_OK
            response_json = json.loads(await response.text())
            return response_json['access']


async def login_users(users):
    async with aiohttp.ClientSession() as session:
        get_users_tokens = [login_user(session, user) for user in users]
        tokens = await asyncio.gather(*get_users_tokens)
        populate(objects=users, field='token', values=tokens)
    print(f'logged {len(users)} users in')


async def submit_user(session, user):
    with async_timeout.timeout(Settings.REQUEST_TIMEOUT):
        async with session.post(Settings.CREATE_USER_URL, data=user.dict()) as response:
            assert response.status == status.HTTP_201_CREATED
            response_json = json.loads(await response.text())
            return response_json['id']


def generate_users():
    return [
        User(username=generate_str(),
             password=generate_str(),
             email=generate_email())
        for _ in range(Settings.USERS_COUNT)
    ]


async def create_users(users):
    async with aiohttp.ClientSession() as session:
        coroutines = [submit_user(session, user) for user in users]
        user_ids = await asyncio.gather(*coroutines)
        populate(objects=users, field='user_id', values=user_ids)
    print(f'created {len(users)} users')


async def test_create_users():
    users = generate_users()
    await create_users(users)
    assert is_populated(objects=users, field='user_id')
    return users


async def test_login_users(users):
    await login_users(users)
    assert is_populated(objects=users, field='token')
