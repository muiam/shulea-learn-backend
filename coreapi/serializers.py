from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['type'] =user.type
        token['first_name'] = user.first_name
        token['second_name'] = user.second_name
        # ...

        return token


class RegisterTutorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['email', 'password', 'first_name', 'last_name' ,'type','phone_number']
            extra_kwargs = {'password': {'required': True}}


        def validate_email(self, value):
            """
            Check if the email is available.
            """
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.", code='email_in_use')
            return value

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            user.set_password(validated_data['password'])
            # user.save()
            return user
        


class RegisterLearnerSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['email', 'password', 'first_name', 'last_name' ,'type','phone_number']
            extra_kwargs = {'password': {'required': True}}


        def validate_email(self, value):
            """
            Check if the email is available.
            """
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in use.", code='email_in_use')
            return value

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            user.set_password(validated_data['password'])
            # user.save()
            return user