import json
import logging

from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes((AllowAny, ))
def login_view(request):
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
