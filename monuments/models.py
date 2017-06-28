import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Token model
def get_expiration_date():
    return timezone.now() + datetime.timedelta(days=1)


class Token(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, unique=True)
    hash = models.CharField(max_length=100)
    expiration_date = models.DateTimeField(default=get_expiration_date)

    def is_expired(self):
        return self.expiration_date < timezone.now()


# L'utilisateur
class Person(User):
    class Meta:
        proxy = True
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.email + ")"


# Ville
class City(models.Model):
    zip_code = models.IntegerField(blank=False)
    city_name = models.CharField(max_length=200, blank=False)

    def retrieve_weather(self):
        weather = Weather.objects.filter(city=self)
        return weather[len(weather) - 1]

    def __str__(self):
        return str(self.zip_code) + " " + self.city_name


class Weather(models.Model):
    humidity = models.IntegerField(blank=True, null=True)
    temp_min = models.CharField(max_length=200, blank=True, null=True)
    temp_max = models.CharField(max_length=200, blank=True, null=True)
    visibility = models.IntegerField(blank=True, null=True)
    wind_speed = models.CharField(max_length=200, blank=True, null=True)
    main = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True)


# Address
class Address(models.Model):
    address_1 = models.CharField(max_length=200, blank=False)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True,
                             on_delete=models.CASCADE)  # si on supprime une City, on détruit l'adresse


    def __str__(self):
        return self.address_1 + " " + self.address_2

# Le monument
class Monument(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address = models.OneToOneField(Address, blank=True, null=True)  # si on supprime une adresse on détruit le monument

    def retrieve_notes(self):
        notes = Note.objects.filter(monument=self)
        return notes

    def __str__(self):
        return self.name

# Note sur le monument
# Note est la table intermédiaire pour la relation Many to Many entre les utilisateurs et les monuments
class Note(models.Model):
    note = models.TextField(blank=False)
    user = models.ForeignKey(Person, blank=False, null=True,
                             on_delete=models.SET_NULL)  # si on détruit l'utilisateur, set la FK user à null
    monument = models.ForeignKey(Monument, blank=False, null=True,
                                 on_delete=models.CASCADE)  # si on détruit le monument on supprime la note

    def __str__(self):
        return self.note
