from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Automatically login after registration (optional)
            # You can also return the user data and let frontend redirect to login
            return Response({
                'message': 'User created successfully',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profilo(request):
    return Response({'username': request.user.username, 'user_id': request.user_id})


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # add custom data  if needed, here
            return Response({
                'access': response.data['access'],
                'refresh': response.data['refresh'],
                'user': {
                    'username': request.data.get('username')
                }
            })
        return response


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'You are authenticated!'})
