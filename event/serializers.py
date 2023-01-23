
from rest_framework import serializers

from .models import *
from organization.models import *
from user.serializers import UserSerializer

class GroupForEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [
            'name'
        ]

class ProfileForEventSerializer(serializers.ModelSerializer):

    user_details = UserSerializer(source = 'user', read_only = True)

    class Meta:
        model = Profile
        fields = [
            'user_details',
            'profile_image'
        ]

class EventSerializer(serializers.ModelSerializer):

    total_records = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    user_profile_details = ProfileForEventSerializer(source='user_profile', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'group': { 'write_only': True }
        }


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    
    user_profile_details = ProfileForEventSerializer(source='user', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
