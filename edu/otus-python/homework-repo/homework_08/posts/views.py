from django.views.generic import ListView, DetailView

from .models import Post


class PostListView(ListView):
    """Display a list of blog posts."""

    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    """Display a single blog post."""

    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
