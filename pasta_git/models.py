import os
import shutil

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Repository(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    fork_of = models.ForeignKey('self', null=True)

    class Meta(object):
        permissions = (
            ('read', 'Can read from this repository'),
            ('write', 'Can write to this repository'),
        )

    @property
    def path(self):
        return os.path.join(settings.REPOSITORY_HOME, self.owner.username, self.name + '.git')

    def fork(self, recipient):
        new_repo = Repository(owner=recipient, name=self.name, fork_of=self)
        shutil.copytree(self.path, new_repo.path)
        new_repo.save()
        return new_repo

from pasta_git.signals import *
