from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class BTopic(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BEntry(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, unique=True)
    btopic = models.ForeignKey(BTopic, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000000)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Broadcast Entries'
    
    def __str__(self):
        if len(self.text) > 55:
            print(self.text[55]) + '....'
        else:
            print(self.text)