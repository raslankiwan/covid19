"""Logout"""
import logging

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return HttpResponse(status=status.HTTP_200_OK)
