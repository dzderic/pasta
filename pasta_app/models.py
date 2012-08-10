import os
import shutil

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Repository(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    fork_of = models.ForeignKey('self', null=True)

    class Meta(object):
        permissions = (
            ('admin', 'Can admin this repository'),
            ('read', 'Can read from this repository'),
            ('write', 'Can write to this repository'),
        )
        unique_together = ('owner', 'slug')

    @property
    def path(self):
        return os.path.join(settings.REPOSITORY_HOME, self.owner.username, self.slug + '.git')

    def fork(self, recipient):
        new_repo = Repository(owner=recipient, name=self.name, fork_of=self)
        shutil.copytree(self.path, new_repo.path)
        new_repo.save()
        return new_repo

    def get_edit_url(self):
        return reverse('edit-pasta', args=[self.owner, self.slug])

from pasta_app.listeners import *
