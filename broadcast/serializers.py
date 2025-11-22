from rest_framework import serializers
from .models import BTopic, BEntry

class BTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = BTopic
        exclude = ['owner']

class BEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BEntry
        fields = '__all__'
