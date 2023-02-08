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
        fields = ['name']
        optional_fields = ['users']

    def create(self, validated_data):
        user = self.context.get('user')
        country = Country.objects.create(**validated_data)
        country.users.add(user)
        country.save()
        return country

    def update(self, instance, validated_data):
        user = self.context.get('user')
        instance.users.add(user)
        instance.save()

        return instance


class TopCountriesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    total_deaths = serializers.IntegerField()
    total_confirmed = serializers.IntegerField()
