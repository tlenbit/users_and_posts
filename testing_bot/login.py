import aiohttp
import async_timeout
import asyncio
import json

from rest_framework import status
from utils import Settings
from utils import is_populated
from utils import populate


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


async def test_login_users(users):
    await login_users(users)
    assert is_populated(objects=users, field='token')