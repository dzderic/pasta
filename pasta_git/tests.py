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
        self._some_guy, _ = User.objects.get_or_create(username='some-guy', password='password')
        settings.REPOSITORY_HOME = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(settings.REPOSITORY_HOME)

    def test_creating_model_creates_repository(self):
        repo = Repository(owner=self._some_guy, name='awesome-repository')
        self.assertFalse(os.path.exists(repo.path))
        repo.save()
        self.assertTrue(os.path.exists(repo.path))

    def test_deleting_model_archives_repository(self):
        repo = Repository(owner=self._some_guy, name='another-repository')
        repo.save()
        self.assertTrue(os.path.exists(repo.path))
        repo.delete()
        self.assertTrue(os.path.exists('%s.archived.%s' % (repo.path, int(time.time()))))
