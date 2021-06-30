from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(to='users.User', null=True, on_delete=models.SET_NULL)


class Like(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.CASCADE)

    # assume that users can like only posts
    # hence abstract FK is not needed
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
