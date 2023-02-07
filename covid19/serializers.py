# pylint: disable=imported-auth-user

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Country


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'users']

    def create(self, validated_data):
        users = validated_data.pop("users")
        country = Country.objects.create(**validated_data)
        for user in users:
            country.users.add(user)
        country.save()
        return country


class TopCountriesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    total_deaths = serializers.IntegerField()
    total_confirmed = serializers.IntegerField()
