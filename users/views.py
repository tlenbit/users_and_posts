from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from .serializers import UserSerializer, SignUpSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            user.save()
            serializer.validated_data['id'] = user.id
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk):
        user = self.get_object()

        data = {
            'last_login': user.last_login,
            'last_activity': user.last_activity
        }

        return Response(data, status=status.HTTP_200_OK)
