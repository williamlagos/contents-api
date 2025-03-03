from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.core.serializers import serialize
from django.utils import timezone
from .models import Content


@require_http_methods(["GET"])
def root(request):
    """Health check view."""
    return JsonResponse({"health": "OK"})


@require_http_methods(["POST"])
def create_content(request):
    """Create a new content item."""
    data = request.POST
    content = Content.objects.create(
        title=data.get("title"),
        content=data.get("content"),
        author=data.get("author")
    )
    return JsonResponse(content.to_dict())


@require_http_methods(["GET"])
def get_contents(request):
    """Retrieve all content items."""
    contents = Content.objects.all()
    return JsonResponse(serialize('json', contents), safe=False)


@require_http_methods(["GET"])
def count_contents(request):
    """Count the number of content items."""
    count = Content.objects.count()
    return JsonResponse({"count": count})


@require_http_methods(["GET"])
def get_content_by_id(request, content_id):
    """Retrieve a content item by its ID."""
    try:
        content = Content.objects.get(id=content_id)
        return JsonResponse(content.to_dict())
    except Content.DoesNotExist:
        return HttpResponseNotFound()


@require_http_methods(["PATCH"])
def update_content(request, content_id):
    """Update a content item by its ID."""
    try:
        content = Content.objects.get(id=content_id)
        data = request.POST
        content.title = data.get("title", content.title)
        content.content = data.get("content", content.content)
        content.author = data.get("author", content.author)
        content.updated_at = timezone.now()
        content.save()
        return JsonResponse(content.to_dict())
    except Content.DoesNotExist:
        return HttpResponseNotFound()


@require_http_methods(["DELETE"])
def delete_content(request, content_id):
    """Delete a content item by its ID."""
    try:
        content = Content.objects.get(id=content_id)
        content.delete()
        return JsonResponse({"message": "Content deleted successfully"})
    except Content.DoesNotExist:
        return HttpResponseNotFound()
