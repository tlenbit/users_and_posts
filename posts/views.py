from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Like
from .models import Post
from .serializers import LikeSerializer
from .serializers import LikesAnalyticsSerializer
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        serializer = LikesAnalyticsSerializer(data=request.query_params)

        if serializer.is_valid():
            date_from = serializer.validated_data['date_from']
            date_to = serializer.validated_data['date_to']
            stats = Like.objects.filter(created_at__gte=date_from) \
                                .filter(created_at__lte=date_to) \
                                .annotate(date=TruncDay('created_at')) \
                                .values('date') \
                                .annotate(count=Count('id'))
            return Response(list(stats),
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
