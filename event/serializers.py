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

    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user_details',
            'profile_image'
        ]


class CommentSerializer(serializers.ModelSerializer):

    user_profile_details = ProfileForEventSerializer(source='user', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    total_records = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    user_profile_details = ProfileForEventSerializer(source='user_profile', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'group': {'write_only': True}
        }


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
        ]


class RecordSerializer(serializers.ModelSerializer):
    event_details = EventDetailSerializer(read_only=True, source='event')

    class Meta:
        model = Record
        fields = '__all__'


class EventHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event.history.model
        fields = '__all__'


class RecordHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Record.history.model
        fields = '__all__'


class CommentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment.history.model
        fields = '__all__'
