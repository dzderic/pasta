import os
import time
import tempfile
import shutil

from django.utils import unittest
from django.contrib.auth.models import User
from django.conf import settings
from guardian.utils import get_anonymous_user
from guardian.shortcuts import assign

from pasta_git.models import Repository

class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self._human_a, _ = User.objects.get_or_create(username='human-a', password='password')
        self._human_b, _ = User.objects.get_or_create(username='human-b', password='password')
        settings.REPOSITORY_HOME = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(settings.REPOSITORY_HOME)

    def test_creating_model_creates_repository(self):
        repo = Repository(owner=self._human_a, name='Awesome repository')
        self.assertFalse(os.path.exists(repo.path))
        repo.save()
        self.assertTrue(os.path.exists(repo.path))

    def test_deleting_model_archives_repository(self):
        repo = Repository(owner=self._human_a, name='Another repository')
        repo.save()
        self.assertTrue(os.path.exists(repo.path))
        repo.delete()
        self.assertTrue(os.path.exists('%s.archived.%s' % (repo.path, int(time.time()))))

    def test_slug_is_generated(self):
        repo = Repository(owner=self._human_a, name='Some repository')
        self.assertEqual(repo.slug, '')
        repo.save()
        self.assertEqual(repo.slug, 'some-repository')

    def test_slugs_are_unique(self):
        repo = Repository(owner=self._human_a, name='I like turtles')
        repo2 = Repository(owner=self._human_a, name='I like turtles')
        repo.save()
        repo2.save()
        self.assertEqual(repo.slug, 'i-like-turtles')
        self.assertEqual(repo2.slug, 'i-like-turtles-2')

    def test_slugs_are_unique_by_user(self):
        repo = Repository(owner=self._human_a, name='I also like turtles')
        repo2 = Repository(owner=self._human_b, name='I also like turtles')
        repo.save()
        repo2.save()
        self.assertEqual(repo.slug, 'i-also-like-turtles')
        self.assertEqual(repo2.slug, 'i-also-like-turtles')

    def test_forking_works(self):
        repo = Repository(owner=self._human_a, name='Some code')
        repo.save()
        fork = repo.fork(recipient=self._human_b)
        self.assertTrue(os.path.exists(fork.path))

    def test_basic_permissions(self):
        repo = Repository(owner=self._human_a, name='Node is web scale')
        repo.save()
        self.assertTrue(self._human_a.has_perm('write', repo))
        self.assertFalse(self._human_b.has_perm('write', repo))

    def test_fallback_to_anonymous_user(self):
        repo = Repository(owner=self._human_a, name='Node isnt web scale')
        repo.save()
        self.assertTrue(self._human_a.has_perm('read', repo))
        self.assertFalse(self._human_b.has_perm('read', repo))
        assign('read', get_anonymous_user(), repo)
        self.assertTrue(self._human_b.has_perm('read', repo))
