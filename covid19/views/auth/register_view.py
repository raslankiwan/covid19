import json
import logging

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def register_view(request):
    data = json.loads(request.body.decode("utf-8"))

    username = data['username']
    email = data['email']
    password = data['password']
    user = User.objects.create_user(
        username, email, password)

    token = Token.objects.create(user=user)

    return JsonResponse({
        'token': str(token),
        'user': model_to_dict(user)
    })
