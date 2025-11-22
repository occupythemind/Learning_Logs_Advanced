from rest_framework import serializers
from .models import Topic, Entry

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        exclude = ['owner']

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'