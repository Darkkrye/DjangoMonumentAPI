from rest_framework import serializers
from monuments.models import *


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('pk', 'username', 'first_name', 'last_name', 'email')


class PersonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('pk', 'username', 'first_name', 'last_name', 'email', 'password')

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ('main', 'description', 'humidity', 'temp_min', 'temp_max', 'visibility', 'wind_speed')

class CitySerializer(serializers.ModelSerializer):
    weather = WeatherSerializer(source='retrieve_weather', many=False)

    class Meta:
        model = City
        fields = ('zip_code', 'city_name', 'weather')


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False)

    class Meta:
        model = Address
        fields = ('id', 'address_1', 'address_2', 'city')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'note', 'user', 'monument')




# For Monument Serializer
class PersonSerializerForMonument(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('username', 'first_name', 'last_name', 'email')

class NoteSerializerForMonument(serializers.ModelSerializer):
    user = PersonSerializerForMonument(many=False)
    class Meta:
        model = Note
        fields = ('note', 'user')

class MonumentSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    notes = NoteSerializerForMonument(source='retrieve_notes', read_only=True, many=True)

    class Meta:
        model = Monument
        fields = ('name', 'address', 'notes')