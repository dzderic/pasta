from django.db import models
from django.contrib.auth.models import User

class Repository(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    path = models.TextField()

    class Meta(object):
        permissions = (
            ('can_read', 'Can read from this repository'),
            ('can_write', 'Can write to this repository'),
        )
