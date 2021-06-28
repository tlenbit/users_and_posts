# syntax=docker/dockerfile:1
FROM archlinux
# ENV PYTHONUNBUFFERED=1
WORKDIR /code

#  RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm poetry 
RUN pacman -S --noconfirm gnu-netcat
RUN pacman -S --noconfirm postgresql-libs
RUN pacman -S --noconfirm gcc

# RUN pip install --user poetry

# COPY requirements.txt /code/
COPY poetry.lock pyproject.toml /code/
RUN poetry install
COPY . /code/

ENTRYPOINT ["/code/entrypoint.sh"]
