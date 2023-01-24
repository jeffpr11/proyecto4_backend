
from rest_framework import serializers
from .models import *
from user.serializers import ProfileSerializer

class GroupSerializer(serializers.ModelSerializer):

    leader_details = ProfileSerializer(source='group_leader', read_only=True)
    
    class Meta:
        model = Group
        fields = '__all__'
        extra_kwargs = {
            'group_leader': {'write_only': True},
            'members': {'read_only': True},
        }


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'name'
        ]

class ResourceSerializer(serializers.ModelSerializer):
    
    groups_details = GroupDetailSerializer(source='groups', read_only=True, many=True)
    
    class Meta:
        model = Resource
        fields = '__all__'


class GroupHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group.history.model
        fields = '__all__'


class ResourceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource.history.model
        fields = '__all__'
