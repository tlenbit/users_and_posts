from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer
from .serializers import LikeSerializer
from .serializers import LikesAnalyticsSerializer
from .models import Post
from .models import Like


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
            likes_count = Like.objects.filter(created_at__gte=serializer.validated_data['date_from']) \
                                      .filter(created_at__lte=serializer.validated_data['date_to']).count()
            return Response({'likes_count': likes_count},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
