
from rest_framework import serializers
# from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User
class SignupUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password',
                  'email', 'first_name', 'last_name', 'mobile')
        # extra_kwargs={"confirm_password":{'write_only':True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'password': "password and confirm_password did'nt match."})
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password']