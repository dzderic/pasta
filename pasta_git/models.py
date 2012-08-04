from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Repository(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)

    class Meta(object):
        permissions = (
            ('can_read', 'Can read from this repository'),
            ('can_write', 'Can write to this repository'),
        )

    @property
    def path(self):
        return os.path.join(settings.REPOSITORY_HOME, owner.username, name + '.git')
