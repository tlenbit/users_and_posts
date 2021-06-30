PRERESUISITES:

install poetry:
https://python-poetry.org/docs/#installation

START PROJECT:

sudo docker-compose up

START BOT:

poetry run python testing_bot/testing_bot.py

APIs:

http://127.0.0.1:8000/api/users/

http://127.0.0.1:8000/api/users/---PASTE USER ID---/analytics/

http://127.0.0.1:8000/api/posts/
  
http://127.0.0.1:8000/api/likes/
  
http://127.0.0.1:8000/api/likes/analytics/?date_from=2021-06-30&date_to=2099-06-01
