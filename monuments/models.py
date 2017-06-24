from django.db import models

# Utilisateur
class User(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)

class Note(models.Model):
    note = models.TextField(blank=False)

class Monument(models.Model):
    name = models.CharField(max_length=200, blank=False)


class Address(models.Model):
    address_1 = models.CharField(max_length=200, blank=False)
    address_2 = models.CharField(max_length=200)

class City(models.Model):
    zip_code = models.IntegerField(blank=False)
    city_name = models.CharField(max_length=200, blank=False)


