"""Logout"""
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView


class Logout(APIView):

    def post(self, request):
        request.user.auth_token.delete()
        return HttpResponse(status=status.HTTP_200_OK)
