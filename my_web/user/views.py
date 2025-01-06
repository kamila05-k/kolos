from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from .models import CustomUser

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        # Use the LoginSerializer to validate the login attempt
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # Attempt to authenticate the user using the custom backend
            user = authenticate(request, username=email, password=password)

            if user:
                # Successful login - Return success message in Russian
                return Response({"message": "Вход успешен", "user": {"email": user.email}}, status=status.HTTP_200_OK)
            else:
                # Authentication failed - Return failure message in Russian
                return Response({"message": "Ошибка аутентификации"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
