# pylint: disable=imported-auth-user
# pylint: disable=import-error
import logging

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from covid19.serializers import UserSerializer

logger = logging.getLogger('django')


@permission_classes((AllowAny, ))
class Register(APIView):

    def post(self, request):
        username = request.data.get('username', '')
        if not User.objects.filter(username=username).exists():
            user = UserSerializer(data=request.data)
            if (user.is_valid()):
                user.save()
                return Response(user.data, status=status.HTTP_201_CREATED)
            return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
