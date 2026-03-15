import os
import django
from django.core.management import call_command
from django.test import Client, TestCase

# Configure settings for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
django.setup()
call_command("migrate", run_syncdb=True, verbosity=0)

from posts.models import Post


class PostViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.post1 = Post.objects.create(title="Post 1", content="Content 1")
        self.post2 = Post.objects.create(title="Post 2", content="Content 2")

    def test_list_view_displays_posts(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post2.title)

    def test_detail_view_displays_post_and_back_link(self):
        response = self.client.get(f"/{self.post1.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.content)
        # link back to list
        self.assertContains(response, 'href="/"')
