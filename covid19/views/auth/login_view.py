import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User  # pylint: disable=imported-auth-user
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

logger = logging.getLogger('django')

@permission_classes((AllowAny, ))
class Login(APIView):

    def post(self, request):

        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            token = Token.objects.create(user=user)

            login(request, user)
            return JsonResponse({
                'token': str(token),
                'user': model_to_dict(user)
            })
        else:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)

