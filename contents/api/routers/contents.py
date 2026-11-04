from typing import List

from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router

from ..models import Content
from ..schemas import ContentIn, ContentOut, ContentPatch, CountOut, MessageOut

router = Router(tags=["Contents"])


@router.get("/", response=List[ContentOut])
def list_contents(request):
    """Retrieve all content items ordered by creation date."""
    return Content.objects.all()


@router.get("/count", response=CountOut)
def count_contents(request):
    """Get the total count of content items."""
    return {"count": Content.objects.count()}


@router.post("/", response={201: ContentOut})
def create_content(request, payload: ContentIn):
    """Create a new content item."""
    content = Content.objects.create(
        title=payload.title,
        content=payload.content,
        author=payload.author,
    )
    return 201, content


@router.get("/{content_id}", response={200: ContentOut, 404: MessageOut})
def get_content(request, content_id: int):
    """Retrieve a single content item by ID."""
    try:
        content = Content.objects.get(id=content_id)
        return 200, content
    except Content.DoesNotExist:
        return 404, {"message": f"Content item with id {content_id} not found"}


@router.patch("/{content_id}", response={200: ContentOut, 404: MessageOut})
def update_content(request, content_id: int, payload: ContentPatch):
    """Update fields on a content item."""
    try:
        content = Content.objects.get(id=content_id)
    except Content.DoesNotExist:
        return 404, {"message": f"Content item with id {content_id} not found"}

    if payload.title is not None:
        content.title = payload.title
    if payload.content is not None:
        content.content = payload.content
    if payload.author is not None:
        content.author = payload.author

    content.updated_at = timezone.now()
    content.save()
    return 200, content


@router.delete("/{content_id}", response={200: MessageOut, 404: MessageOut})
def delete_content(request, content_id: int):
    """Delete a content item by ID."""
    try:
        content = Content.objects.get(id=content_id)
        content.delete()
        return 200, {"message": "Content deleted successfully"}
    except Content.DoesNotExist:
        return 404, {"message": f"Content item with id {content_id} not found"}
