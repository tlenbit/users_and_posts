import aiohttp
import async_timeout
import asyncio
import json
import pydantic
import random

from rest_framework import status
from typing import Optional
from users import User
from utils import Settings
from utils import generate_str
from utils import is_populated
from utils import populate
from posts import Post


class Like(pydantic.BaseModel):
    post: Post
    user: User
    like_id: Optional[int]


async def submit_like(session, like):
    user = like.user
    post = like.post
    with async_timeout.timeout(Settings.REQUEST_TIMEOUT):
        headers = {'Authorization': f'Bearer {user.token}'}
        post_data = {'user': user.user_id, 'post': post.post_id}
        async with session.post(Settings.CREATE_LIKE_URL, data=post_data,
                                headers=headers) as response:
            assert response.status == status.HTTP_201_CREATED
            response_json = json.loads(await response.text())
            return response_json['id']


async def create_likes(likes):
    async with aiohttp.ClientSession() as session:
        coroutines = [submit_like(session, like)
                      for like in likes]
        like_ids = await asyncio.gather(*coroutines)
        populate(likes, 'like_id', like_ids)
    print(f'created {len(likes)} likes')


def generate_likes(users, posts):
    likes = []
    for _ in range(Settings.LIKES_COUNT):
        user = random.choice(users)
        post = random.choice(posts)
        likes.append(Like(user=user, post=post))
    return likes


async def test_create_likes(posts, users):
    likes = generate_likes(users, posts)
    await create_likes(likes)
    assert is_populated(objects=likes, field='like_id')
