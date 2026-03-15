from django.http import HttpResponse


def index(request):
    """Simple view returning a greeting."""
    return HttpResponse("Hello, blog!")
