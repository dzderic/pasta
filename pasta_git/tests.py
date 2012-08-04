import os
import time
import tempfile
import shutil

from django.utils import unittest
from django.contrib.auth.models import User
from django.conf import settings

from pasta_git.models import Repository

class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self._human_a, _ = User.objects.get_or_create(username='human-a', password='password')
        self._human_b, _ = User.objects.get_or_create(username='human-b', password='password')
        settings.REPOSITORY_HOME = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(settings.REPOSITORY_HOME)

    def test_creating_model_creates_repository(self):
        repo = Repository(owner=self._human_a, name='awesome-repository')
        self.assertFalse(os.path.exists(repo.path))
        repo.save()
        self.assertTrue(os.path.exists(repo.path))

    def test_deleting_model_archives_repository(self):
        repo = Repository(owner=self._human_a, name='another-repository')
        repo.save()
        self.assertTrue(os.path.exists(repo.path))
        repo.delete()
        self.assertTrue(os.path.exists('%s.archived.%s' % (repo.path, int(time.time()))))

    def test_forking_works(self):
        repo = Repository(owner=self._human_a, name='some-code')
        repo.save()
        fork = repo.fork(recipient=self._human_b)
        self.assertTrue(os.path.exists(fork.path))
