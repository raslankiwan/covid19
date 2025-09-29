import logging

from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes as perm_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger('django')

@perm_classes((AllowAny, ))
class Login(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.create(user=request.user)

        content = {
            'token': str(token)
        }
        return Response(content)
