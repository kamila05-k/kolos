from rest_framework import serializers

from .models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, min_length=8, max_length=12)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check if the user exists
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User with this email does not exist.")

        # Check if the account is locked
        if user.is_locked:
            raise serializers.ValidationError("This account is locked due to multiple failed attempts.")

        # Check if the password is correct
        if not user.check_password(password):
            user.failed_attempts += 1
            user.save()

            # Lock the account if failed attempts are >= 4
            user.lock_account()

            raise serializers.ValidationError("Incorrect password.")

        return data
