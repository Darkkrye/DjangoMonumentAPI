from django.db import models

# Utilisateur
class User(models.Model):
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)

# Ville
class City(models.Model):
    zip_code = models.IntegerField(blank=False)
    city_name = models.CharField(max_length=200, blank=False)

# Adress
class Address(models.Model):
    address_1 = models.CharField(max_length=200, blank=False)
    address_2 = models.CharField(max_length=200)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE) # si on supprime une City, on détruit l'adresse

# Le monument
class Monument(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address = models.OneToOneField(Address, blank=True, null=True)  # si on supprime une adresse on détruit le monument

# Note sur le monument
# Note est la table intermédiaire pour la relation Many to Many entre les utilisateurs et les monuments
class Note(models.Model):
    note = models.TextField(blank=False)
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL) #si on détruit l'utilisateur, set la FK user à null
    monument = models.ForeignKey(Monument, blank=False, null=True, on_delete=models.CASCADE) # si on détruit le monument on supprime la note





