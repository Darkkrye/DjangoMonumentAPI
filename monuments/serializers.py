from rest_framework import serializers
from monuments.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('pk', 'username', 'first_name', 'last_name', 'email')


class PersonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('pk', 'username', 'first_name', 'last_name', 'email', 'password')
