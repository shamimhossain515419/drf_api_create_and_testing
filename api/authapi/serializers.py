from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])  # password hash করে save করবে
        user.save()
        return user


class CustomEmailTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = User.EMAIL_FIELD  # important

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password")

            user = authenticate(username=user_obj.username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password")

            data = super().get_token(user)
            return {
                "refresh": str(data),
                "access": str(data.access_token),
            }
        else:
            raise serializers.ValidationError("Must include email and password fields.")

    def get_fields(self):
        return {
            "email": serializers.EmailField(),
            "password": serializers.CharField(),
        }


# //  update profile


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        read_only_fields = ["email"]  # চাইলে email কে read-only করতে পারো
