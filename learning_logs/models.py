from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

#models specify how django should deal with data
class Topic(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Entry(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='entries')
    text = models.CharField(max_length=10000000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Entries'
    
    def __str__(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text
