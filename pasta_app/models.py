import os
import shutil

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from dulwich.repo import Repo

from pasta_app.helpers import cached_property

class Repository(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    fork_of = models.ForeignKey('self', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        permissions = (
            ('admin', 'Can admin this repository'),
            ('read', 'Can read from this repository'),
            ('write', 'Can write to this repository'),
        )
        unique_together = ('owner', 'slug')

    @cached_property
    def path(self):
        return os.path.join(settings.REPOSITORY_HOME, self.owner.username, self.slug + '.git')

    @cached_property
    def repo(self):
        return Repo(self.path)

    def fork(self, recipient):
        new_repo = Repository(owner=recipient, name=self.name, fork_of=self)
        shutil.copytree(self.path, new_repo.path)
        new_repo.save()
        return new_repo

    def get_absolute_url(self):
        return reverse('view-pasta', args=[self.owner, self.slug])

    def get_files(self, ref='master'):
        refs = self.repo.get_refs()
        if not refs:  # no commits yet
            return
        elif 'refs/heads/' + ref in refs:
            ref_hash = refs['refs/heads/' + ref]
        elif ref in refs:
            ref_hash = refs[ref]
        elif len(ref) in (20, 40) and ref in self.repo:
            ref_hash = ref
        else:
            raise Http404("The specified ref wasn't found")

        commit = self.repo.commit(ref_hash)
        trees = sorted(self.repo.tree(commit.tree).iteritems(), key=lambda x: x.path)

        for thing in trees:
            if not stat.S_ISREG(thing.mode):  # skip if it's not a file
                pass

            # Get the git blob from the SHA
            blob = self.repo.get_blob(thing.sha)
            yield {
                'path': thing.path,
                'contents': blob.data,
            }

from pasta_app.listeners import *
