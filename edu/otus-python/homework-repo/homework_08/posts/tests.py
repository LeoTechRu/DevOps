"""Tests for the posts application views."""

from django.test import TestCase
from django.urls import reverse

from .models import Post


class PostViewTests(TestCase):
    """Ensure list and detail views provide correct context."""

    def setUp(self) -> None:
        """Create sample posts for use in tests."""
        self.post1 = Post.objects.create(title="First", content="First content")
        self.post2 = Post.objects.create(title="Second", content="Second content")

    def tearDown(self) -> None:
        """Remove all posts created for tests."""
        Post.objects.all().delete()

    def test_post_list_context(self) -> None:
        """List view should include all posts in context."""
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_list.html")
        posts = set(response.context["posts"])
        self.assertEqual(posts, {self.post1, self.post2})

    def test_post_detail_context(self) -> None:
        """Detail view should include the requested post in context."""
        response = self.client.get(reverse("post_detail", args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_detail.html")
        self.assertEqual(response.context["post"], self.post1)
