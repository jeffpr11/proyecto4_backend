
from rest_framework import serializers
from .models import *


class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            # 'group': { 'write_only': True },
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
