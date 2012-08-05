import os
import time

from django.db.models.signals import pre_save, post_save, post_delete
from django.template.defaultfilters import slugify
from dulwich.repo import Repo
from guardian.shortcuts import assign

from pasta_git.models import Repository

def create_repository(instance, **kwargs):
    # Return if the repository has already been created
    if os.path.exists(instance.path):
        return

    # Create the repository and initialize it as a bare Git repo
    os.makedirs(instance.path)
    Repo.init_bare(instance.path)

post_save.connect(create_repository, sender=Repository)

def archive_repository(instance, **kwargs):
    # Return if the repository doesn't exist anymore
    if not os.path.exists(instance.path):
        return

    # Move the repository to '<path>.archived.<timestamp>'
    os.rename(instance.path, '%s.archived.%s' % (instance.path, int(time.time())))

post_delete.connect(archive_repository, sender=Repository)

def assign_permissions(instance, **kwargs):
    # Give the owner read/write access to their own repository
    assign('read', instance.owner, instance)
    assign('write', instance.owner, instance)

post_save.connect(assign_permissions, sender=Repository)

def generate_slug(instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(generate_slug, sender=Repository)
