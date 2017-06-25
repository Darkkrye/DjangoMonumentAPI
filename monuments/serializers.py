from rest_framework import serializers
from monuments.models import Person, Monument, Address, City, Note


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('pk', 'username', 'first_name', 'last_name', 'email')


class PersonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('pk', 'username', 'first_name', 'last_name', 'email', 'password')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'zip_code', 'city_name')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address_1', 'address_2', 'city')


class MonumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monument
        fields = ('id', 'name', 'address')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'note', 'user', 'monument')
