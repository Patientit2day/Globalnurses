from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer

# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Créez l'utilisateur

        # Envoyez le message de bienvenue avec le nom d'utilisateur
        message = user.send_welcome_message(username=user.username)

        # Retournez une réponse
        return Response(
            {"message": message},
            status=status.HTTP_201_CREATED
        )