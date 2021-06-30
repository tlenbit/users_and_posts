import aiohttp
import async_timeout
import asyncio
import json
import pydantic

from rest_framework import status
from typing import Optional
from utils import Settings
from utils import generate_str
from utils import is_populated
from utils import populate


class Post(pydantic.BaseModel):
    title: str
    content: str
    author: Optional[str]
    post_id: Optional[int]


async def submit_post(session, user, post):
    post.author = user.user_id
    with async_timeout.timeout(Settings.REQUEST_TIMEOUT):
        headers = {'Authorization': f'Bearer {user.token}'}
        async with session.post(Settings.CREATE_POST_URL, data=post.dict(),
                                headers=headers) as response:
            assert response.status == status.HTTP_201_CREATED
            response_json = json.loads(await response.text())
            return response_json['id']


async def create_posts(posts, users):
    async with aiohttp.ClientSession() as session:
        coroutines = [submit_post(session, user, post)
                      for user, user_posts in zip(users, posts)
                      for post in user_posts]
        post_ids = await asyncio.gather(*coroutines)
        for user_posts in posts:
            populate(user_posts, 'post_id', post_ids)
    print(f'created {len(users)} posts')


def generate_post():
    return Post(
        title=generate_str(),
        content=generate_str()
    )


def generate_user_posts():
    return [generate_post() for _ in range(Settings.MAX_POSTS_COUNT)]


async def test_create_posts(users):
    posts_per_user = [generate_user_posts() for user in users]
    await create_posts(posts_per_user, users)
    all_posts = [post for user_posts in posts_per_user for post in user_posts]
    assert is_populated(objects=all_posts, field='post_id')
    return all_posts


