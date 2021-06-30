import asyncio

from likes import test_create_likes
from posts import test_create_posts
from users import test_create_users
from login import test_login_users


async def main():
    users = await test_create_users()
    await test_login_users(users)
    posts = await test_create_posts(users)
    await test_create_likes(posts, users)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
