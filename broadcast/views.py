from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth.models import User
from rest_framework import mixins, generics
from learning_logs.permissions import IsAdminOrReadOnly
from .models import BTopic, BEntry
from .serializers import BTopicSerializer, BEntrySerializer

class BTopicListCreateView(generics.ListCreateAPIView):
    """GET/POST request"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = BTopic.objects.all()
    serializer_class = BTopicSerializer
    
    def perform_create(self, serializer):
        # Automatically assign owner when creating
        serializer.save(owner=self.request.user)


class BTopicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """PUT/PATCH/DELETE"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = BTopic.objects.all()
    serializer_class = BTopicSerializer
    

class BEntryListCreateView(generics.ListCreateAPIView):
    """GET/POST"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = BEntry.objects.all()
    serializer_class = BEntrySerializer

    def perform_create(self, serializer):
        btopic = serializer.validated_data['btopic']
        if btopic.owner != self.request.user:
            raise Http404(settings.UNKNOWN_RESOURCE)
        serializer.save()
        
class BEntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """PUT/PATCH/DELETE"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = BEntry.objects.all()
    serializer_class = BEntrySerializer

    def perform_create(self, serializer):
        btopic = serializer.validated_data['btopic']
        if btopic.owner != self.request.user:
            raise Http404(settings.UNKNOWN_RESOURCE)
        serializer.save()