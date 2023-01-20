
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


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
