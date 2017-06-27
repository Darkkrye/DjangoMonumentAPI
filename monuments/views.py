from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from monuments.client import getWeatherByCity
from monuments.models import *
from monuments.serializers import *

#
# GESTION DES USERS
#
@require_GET
def users(request, pk=None):
    if pk == None:
        users = Person.objects.all()
        us = PersonSerializer(users, many=True)
        return JsonResponse(us.data, safe=False, status=status.HTTP_200_OK)
    else:
        users = Person.objects.get(pk=pk)
        us = PersonSerializer(users, many=False)
        return JsonResponse(us.data, safe=False, status=status.HTTP_200_OK)

@require_POST
def login(request):
    return HttpResponse(status=status.HTTP_201_CREATED)

@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def user(request, pk=None):
    #
    # Gestion de la méthode POST
    #
    if request.method == 'POST':
        # réception des données postées par l'utilisateur
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # désérialisations
        user_post_serializer = PersonPostSerializer(data=data)

        # Si on a unutilisateur valide, on l'enregistre
        if user_post_serializer.is_valid():

            # ici vu qu'on va créer un utilisateur et qu'on souhaite hashé son mot de passe
            # on va utiliser  create_user, donc pas de save immédiatement
            new_user = User.objects.create_user(
                user_post_serializer.data['username'],
                user_post_serializer.data['email'],
                user_post_serializer.data['password'])
            new_user.first_name = user_post_serializer.data['first_name']
            new_user.last_name = user_post_serializer.data['last_name']
            new_user.save()

            # pour eviter d'envoyer le mot de passe envoyé par la méthode post, on serialize avec le serializer adequat
            user_serializer = PersonSerializer(new_user)

            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(user_post_serializer.data, status=status.HTTP_400_BAD_REQUEST)

    #
    # Gestion de la méthode DELETE
    #
    elif request.method == 'DELETE':
        # étant donné que l'on peut ne pas avoir de pk (paramètre facultatif) on fait un try / catch
        try:
            user_delete = User.objects.get(pk=pk)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        user_delete.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    #
    # Cas impossible normalement avec le decorator
    #
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)













#
# GESTION DES NOTES
#
@require_GET
def notes(request, id=None):
    if id == None:
        notes = Note.objects.all()
        ns = NoteSerializer(notes, many=True)
        return JsonResponse(ns.data, safe=False, status=status.HTTP_200_OK)
    else:
        notes = Note.objects.get(id=id)
        ns = NoteSerializer(notes, many=False)
        return JsonResponse(ns.data, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def note(request, id=None):
    #
    # Gestion de la méthode POST
    #
    if request.method == 'POST':
        # réception des données postées par l'utilisateur
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # désérialisations
        note_serializer = NoteSerializer(data=data)

        # Si on a une monument valide, on l'enregistre
        if note_serializer.is_valid():
            note_serializer.save()

            return JsonResponse(note_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(note_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    #
    # Gestion de la méthode DELETE
    #
    elif request.method == 'DELETE':
        # étant donné que l'on peut ne pas avoir de pk (paramètre facultatif) on fait un try / catch
        try:
            note_delete = Note.objects.get(pk=id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        note_delete.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    #
    # Cas impossible normalement avec le decorator
    #
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)















#
# GESTION DES MONUMENTS
# ATTENTION LA RELATION ENTRE LES MONUMENT ET LES ADDRESS EST UNE RELATION ONE TO ONE DONC SI L'ADDRESSE EST DEJA
# UTILISEE, CA PLANTE
#
@require_GET
def monuments(request, id=None):
    monuments = Monument.objects.all()

    for m in monuments:
        getWeatherByCity(m.address.city.city_name, m.address.city.pk)

    if id == None:
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        page = request.GET.get('page')

        if limit or offset or page != None:
            # Set default values
            if limit != None and int(limit) == 1:
                limit = 2
            if limit == None:
                limit = 100
            if offset == None:
                offset = 0
            if page == None:
                page = 1
            if int(page) > 1:
                offset = 1

            # Force int for values
            limit = int(limit)
            offset = int(offset)
            page = int(page)

            # Calculate Page Offset and End Item
            pageOffset = page * offset
            endItem = pageOffset + limit

            # Retrieve monuments
            newMonuments = monuments[pageOffset:endItem]

            # Create monuments json
            monuments_serializer = MonumentSerializer(newMonuments, many=True)

            # Create return
            if page == 1 or page == 0:
                previous = "http://" + request.get_host() + request.path_info + "?limit=" + str(len(newMonuments)) + "&page=" + str(1)
            else:
                previous = "http://" + request.get_host() + request.path_info + "?limit=" + str(len(newMonuments)) + "&page=" + str(page - 1)

            content = {
                "count": len(newMonuments),
                "next": "http://" + request.get_host() + request.path_info +"?limit=" + str(len(newMonuments)) + "&page=" + str(page + 1),
                "previous": previous,
                "results": monuments_serializer.data
            }

            # Send return
            return JsonResponse(content, safe=False, status=status.HTTP_200_OK)
        else:
            monuments_serializer = MonumentSerializer(monuments, many=True)
            return JsonResponse(monuments_serializer.data, safe=False, status=status.HTTP_200_OK)
    else:
        monument = Monument.objects.get(id=id)
        getWeatherByCity(monument.address.city.city_name, monument.address.city.pk)
        monument_serializer = MonumentSerializer(monument, many=False)
        return JsonResponse(monument_serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def monument(request, id=None):
    #
    # Gestion de la méthode POST
    #
    if request.method == 'POST':
        # réception des données postées par l'utilisateur
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # désérialisations
        monument_serializer = MonumentSerializer(data=data)

        # Si on a une monument valide, on l'enregistre
        if monument_serializer.is_valid():
            monument_serializer.save()

            return JsonResponse(monument_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(monument_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    #
    # Gestion de la méthode DELETE
    #
    elif request.method == 'DELETE':
        # étant donné que l'on peut ne pas avoir de pk (paramètre facultatif) on fait un try / catch
        try:
            monument_delete = monument.objects.get(pk=id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        monument_delete.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    #
    # Cas impossible normalement avec le decorator
    #
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)














#
# GESTION DES ADDRESS
#
@require_GET
def addresses(request, id=None):
    if id == None:
        addresses = Address.objects.all()
        addresses_serializer = AddressSerializer(addresses, many=True)
        return JsonResponse(addresses_serializer.data, safe=False, status=status.HTTP_200_OK)
    else:
        addresses = Address.objects.get(id=id)
        addresses_serializer = AddressSerializer(addresses, many=False)
        return JsonResponse(addresses_serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def address(request, id=None):
    #
    # Gestion de la méthode POST
    #
    if request.method == 'POST':
        # réception des données postées par l'utilisateur
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # désérialisations
        address_serializer = AddressSerializer(data=data)

        # Si on a une address valide, on l'enregistre
        if address_serializer.is_valid():
            address_serializer.save()

            return JsonResponse(address_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(address_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    #
    # Gestion de la méthode DELETE
    #
    elif request.method == 'DELETE':
        # étant donné que l'on peut ne pas avoir de pk (paramètre facultatif) on fait un try / catch
        try:
            address_delete = Address.objects.get(pk=id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        address_delete.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    #
    # Cas impossible normalement avec le decorator
    #
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)













#
# GESTION DES CITY
#
@require_GET
def cities(request, id=None):
    if id == None:
        cities = City.objects.all()
        cs = CitySerializer(cities, many=True)
        return JsonResponse(cs.data, safe=False, status=status.HTTP_200_OK)
    else:
        cities = City.objects.get(id=id)
        cs = CitySerializer(cities, many=False)
        return JsonResponse(cs.data, safe=False, status=status.HTTP_200_OK)

@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def city(request, id=None):
    #
    # Gestion de la méthode POST
    #
    if request.method == 'POST':
        # réception des données postées par l'utilisateur
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # désérialisations
        city_serializer = CitySerializer(data=data)

        # Si on a une city valide, on l'enregistre
        if city_serializer.is_valid():
            city_serializer.save()

            return JsonResponse(city_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(city_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    #
    # Gestion de la méthode DELETE
    #
    elif request.method == 'DELETE':
        # étant donné que l'on peut ne pas avoir de pk (paramètre facultatif) on fait un try / catch
        try:
            city_delete = City.objects.get(pk=id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        city_delete.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    #
    # Cas impossible normalement avec le decorator
    #
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)
