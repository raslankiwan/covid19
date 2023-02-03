import logging

from django.contrib.auth.models import User  # pylint: disable=imported-auth-user
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

logger = logging.getLogger('django')


@permission_classes((AllowAny, ))
class Register(APIView):

    def post(self, request):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
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
