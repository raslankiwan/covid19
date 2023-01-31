import json
import logging

import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
def test(request):

    r = requests.get('https://api.covid19api.com/countries').json()
    return JsonResponse(r, safe=False)
