
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from rest_framework import serializers

from .models import *
from organization.models import Group;



class TokenPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["token"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['name'] = user.first_name + " " + user.last_name
        token['profile_id'] = user.profile.id if hasattr(user, 'profile') else -1
        token['roles'] = ['superuser'] if (user.is_superuser) else [
            group.name for group in user.groups.all()
        ]
        
        return token


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    token = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh_tmp = self.token_class(attrs["refresh"])

        data = {"token": str(refresh_tmp.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh_tmp.blacklist()
                except AttributeError:
                    pass

            refresh_tmp.set_jti()
            refresh_tmp.set_exp()
            refresh_tmp.set_iat()

            data["refresh"] = str(refresh_tmp)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        ]

class ProfileSerializer(serializers.ModelSerializer):
    
    total_events = serializers.IntegerField(read_only=True)
    total_groups = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'


class ProfileHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile.history.model
        fields = '__all__'
