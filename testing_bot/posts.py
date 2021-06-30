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


class Post(pydantic.BaseModel):
    title: str
    content: str
    author: Optional[str]
    post_id: Optional[int]


class Like(pydantic.BaseModel):
    post: Post
    user: User
    like_id: Optional[int]


def generate_user_posts():
    return [generate_post() for _ in range(Settings.MAX_POSTS_COUNT)]


def generate_post():
    return Post(
        title=generate_str(),
        content=generate_str()
    )


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


def generate_likes(users, posts):
    likes = []
    for _ in range(Settings.LIKES_COUNT):
        user = random.choice(users)
        post = random.choice(posts)
        likes.append(Like(user=user, post=post))
    return likes


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


async def test_create_posts(users):
    posts_per_user = [generate_user_posts() for user in users]
    await create_posts(posts_per_user, users)
    all_posts = [post for user_posts in posts_per_user for post in user_posts]
    assert is_populated(objects=all_posts, field='post_id')
    return all_posts


async def test_create_likes(posts, users):
    likes = generate_likes(users, posts)
    await create_likes(likes)
    assert is_populated(objects=likes, field='like_id')
