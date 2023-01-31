import json
import logging

from django.contrib.auth.models import User # pylint: disable=imported-auth-user
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register_view(request):
    data = json.loads(request.body.decode("utf-8"))

    username = data['username']
    email = data['email']
    password = data['password']
    User.objects.exists()
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username, email, password)

        token = Token.objects.create(user=user)

        return JsonResponse({
            'token': str(token),
            'user': model_to_dict(user)
        })
    else:
        return JsonResponse({
            'error': 'User already exists'
        })
