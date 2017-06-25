from pprint import pprint

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from monuments import serializers
from monuments.models import User
from monuments.serializers import UserSerializer

@require_GET
def users(request):
    utilisateurs = User.objects.all()
    utilisateurs_serializer = UserSerializer(utilisateurs, many=True)
    return JsonResponse(utilisateurs_serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def user(request):

    # Gestion de la méthode POST
    if request.method == 'POST':
        # réception des données postées par l'utilisateur
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        # désérialisations
        user_serializer = UserSerializer(data=data)
        pprint(user_serializer)  # permet d'afficher le contenu de data dans la console

        # Si on a unutilisateur valide, on l'enregistre
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(user_serializer.data, status=status.HTTP_400_CREATED)

    # Gestion de la méthode DELETE
    elif request.method == 'DELETE':
        retour = {'message': 'not implemented yet'}
        return JsonResponse(retour, status=status.HTTP_204_NO_CONTENT)

    # Cas impossible normallement avec le decorator
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)