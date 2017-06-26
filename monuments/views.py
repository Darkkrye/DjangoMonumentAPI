from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from monuments.models import Person, City, Address, Note
from monuments.serializers import PersonSerializer, PersonPostSerializer, MonumentSerializer, AddressSerializer, \
    CitySerializer, NoteSerializer


@require_GET
def users(request):
    utilisateurs = Person.objects.all()
    utilisateurs_serializer = PersonSerializer(utilisateurs, many=True)
    return JsonResponse(utilisateurs_serializer.data, safe=False, status=status.HTTP_200_OK)

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
# GESTION DES MONUMENTS
#
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
