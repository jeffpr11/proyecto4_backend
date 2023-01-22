
from rest_framework import serializers

from .models import *
from organization.models import *

class GroupForEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = [
            'name'
        ]

class EventSerializer(serializers.ModelSerializer):
    
    group_details = GroupForEventSerializer(source='group', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'group': { 'write_only': True },
            # 'image' : { 'write_only': True }
        }


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
