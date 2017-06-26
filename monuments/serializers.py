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
    meteo = serializers.SerializerMethodField('get_current_meteo')

    def get_current_meteo(self, foo):
        return "Use function to retrieve Meteo JSON Object"

    class Meta:
        model = Monument
        fields = ('id', 'name', 'address', 'meteo', 'notes')

class MonumentSerializerWithPagination(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    notes = NoteSerializerForMonument(source='retrieve_notes', read_only=True, many=True)
    meteo = serializers.SerializerMethodField('get_current_meteo')

    currentPage = serializers.SerializerMethodField('retrieve_current_page')
    limit = serializers.SerializerMethodField('retrieve_limit')

    def retrieve_current_page(self, foo):
        return self.context.get("current_page")

    def retrieve_limit(self, foo):
        return self.context.get("limit")

    def get_current_meteo(self, foo):
        return "Use function to retrieve Meteo JSON Object"

    class Meta:
        model = Monument
        fields = ('id', 'name', 'address', 'meteo', 'notes', 'currentPage', 'limit')