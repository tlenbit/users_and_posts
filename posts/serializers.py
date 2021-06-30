from django.utils import timezone
from rest_framework import serializers

from .models import Like
from .models import Post
from users.models import User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


class LikesAnalyticsSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField(default=timezone.now().date())
