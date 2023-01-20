
from rest_framework import serializers
from .models import *
from organization.serializers import ImageSerializer


class EventSerializer(serializers.ModelSerializer):

    img_details = ImageSerializer(source='img_file', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
