from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.conf import settings
#from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import TopicSerializer, EntrySerializer
from .models import Topic, Entry
from .permissions import IsOwner
import time

def index(request):
    '''Landing Page'''
    if request.user.is_authenticated:
        return redirect("learning_logs:home")
    else:
        return render(request, 'learning_logs/index.html', { 'timestamp': int(time.time()) })

def pingme(request):
    '''Check and Keep the Site alive.'''
    return HttpResponse("OK")

@login_required
def home(request):
    '''Home page'''
    # fetch the user's personal conf. files for the web UI
    return render(request, 'learning_logs/home.html', { 'timestamp': int(time.time()) })

@login_required
def topic(request, pk):
    '''The topic page'''
    topic_req = Topic.objects.filter(pk=pk).first()
    if not topic_req or topic_req.owner != request.user:
        return Http404
    return render(request, 'learning_logs/topic.html', { 'timestamp': int(time.time()) })

@login_required
def entry(request, pk):
    '''The entry page'''
    entry_req = Entry.objects.filter(pk=pk).first()
    if not entry_req or entry_req.topic.owner != request.user:
        return Http404
    return render(request, 'learning_logs/entry.html', { 'timestamp': int(time.time()) })

@login_required
def dummy(request):
    '''My dummy work'''
    if not request.user.is_staff:
        return Http404
    return render(request, 'learning_logs/dummy.html')

# In case a user has verly large set of topics, we may segment and return some.
# then complete it later.
class TopicAPIView(viewsets.ModelViewSet):
    """API for the topics endpoint"""
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_queryset(self):
        # Only return topics belonging to the current user
        return Topic.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign owner when creating
        serializer.save(owner=self.request.user)
    
class EntryAPIView(viewsets.ModelViewSet):
    """API for the entry endpoint"""
    permission_classes = [IsAuthenticated]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def get_queryset(self):
        if self.kwargs.get('topic_pk'):
            # fetch entry related to that topic and user (thanks to NestedRouter)
            topic_id = self.kwargs.get('topic_pk')
            # x__y is used in django to indicate that y is an attribute of x since x is in the Entry
            return Entry.objects.filter(topic__id=topic_id, topic__owner=self.request.user)
        return Entry.objects.filter(topic__owner=self.request.user) # all entry related to that user


    def perform_create(self, serializer):
        # Ensure the entry is saved to a topic that relates to that user.
        topic = serializer.validated_data['topic']
        if topic.owner != self.request.user:
            raise Http404(settings.UNKNOWN_RESOURCE)
        serializer.save()
