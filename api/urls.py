
from django.urls import path, include
from .views import *
from rest_framework import routers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken





class ObtainAuthToken2(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user = get_user_model().objects.get(username=user)
        return Response({'token': token.key, 'is_staff': user.is_staff})

obtain_auth_token = ObtainAuthToken2.as_view()

urlpatterns = [
    path('', index, name="index"),
    path('rawdata/', RawDataView.as_view(), name="rawDataView"),
    path('auth/login/',obtain_auth_token,name='auth_user_login'),
]
