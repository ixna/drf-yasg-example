from django.contrib.auth.models import User
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response, status, generics
from rest_framework.schemas import openapi
from drf_yasg import openapi
from .serializers import UserSerializer

# Create your views here.


class UserView(generics.GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        query_serializer=UserSerializer,
        responses={200: UserSerializer(many=True)},
        tags=['Users'],
    )
    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by('id')
        serialized = self.get_serializer(users, many=True)
        return response.Response(serialized.data)

    @swagger_auto_schema(
        operation_description="apiview post description override",
        request_body=UserSerializer,
        tags=['Users'],
    )
    def post(self, request, *args, **kwargs):
        serialized = self.get_serializer(data=request.data)
        if serialized.is_valid(raise_exception=False):
            serialized.save()
            return response.Response(serialized.data)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)
