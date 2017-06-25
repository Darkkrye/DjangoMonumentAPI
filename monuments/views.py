from pprint import pprint

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from monuments.models import Person
from monuments.serializers import PersonSerializer, PersonPostSerializer


@require_GET
def users(request):
    utilisateurs = Person.objects.all()
    utilisateurs_serializer = PersonSerializer(utilisateurs, many=True)
    return JsonResponse(utilisateurs_serializer.data, safe=False, status=status.HTTP_200_OK)


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