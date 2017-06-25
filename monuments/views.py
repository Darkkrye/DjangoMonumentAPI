from pprint import pprint

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from monuments.serializers import UserSerializer

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")

@csrf_exempt
def user(request):
    #Gestion de la méthode POST
    if request.method == 'POST':
        #réception des données postées par l'utilisateur
        try:
            data = JSONParser().parse(request)
        except ParseError:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        #désérialisations
        user_serializer = UserSerializer(data=data)
        pprint(user_serializer)  # permet d'afficher le contenu de data dans la console

        #Si on a unutilisateur valide, on l'enregistre
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(user_serializer.data, status=status.HTTP_400_CREATED)
    else:
        return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)





