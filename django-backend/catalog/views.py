from django.contrib.auth.forms import UsernameField
from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Autore, Libro, Scarpe
from .serializers import (
    AutoreSerializer,
    LibroReadSerializer,
    LibroWriteSerializer,
    ScarpeSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User


# Create your views here.
class ScarpeViewSet(viewsets.ModelViewSet):
    queryset = Scarpe.objects.all()

    def get_serializer_class(self):
        # For write operations (create, update, partial_update, destroy)
        if self.action in ["create", "update", "partial_update"]:
            return ScarpeSerializer
        # For read operations (list, retrieve)
        return ScarpeSerializer


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    # serializer_class = LibroSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # For write operations (create, update, partial_update, destroy)
        if self.action in ["create", "update", "partial_update"]:
            return LibroWriteSerializer
        # For read operations (list, retrieve)
        return LibroReadSerializer

    def get_permissions(self):
        if self.action == "list":  # GET (list)
            permission_classes = [AllowAny]
        elif self.action == "create":  # POST
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":  # DELETE
            permission_classes = [IsAdminUser]
        elif self.action in [
            "retrieve",
            "update",
            "partial_update",
        ]:  # GET (detail), PUT, PATCH
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class AutoreViewSet(viewsets.ModelViewSet):
    queryset = Autore.objects.all()
    serializer_class = AutoreSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list":  # GET (list)
            permission_classes = [AllowAny]
        elif self.action == "create":  # POST
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":  # DELETE
            permission_classes = [IsAdminUser]
        elif self.action in [
            "retrieve",
            "update",
            "partial_update",
        ]:  # GET (detail), PUT, PATCH
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def profilo(request):
#     return Response({"username": request.user.username, "user_id": request.user.id})


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     '''
#     Register a new user
#     '''
#     serializer = UserRegistrationSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({
#             'message': f'User {user.username} created successfully',
#             'user_id': user.id,
#             'username': user.username
#         }, status=status.HTTP_201_CREATED )

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
