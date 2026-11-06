from typing import List, Optional

from django.db.models import Q
from django.utils import timezone
from ninja import Query, Router

from ..models import Content, ContentStatus
from ..schemas import ContentIn, ContentOut, ContentPatch, CountOut, MessageOut

router = Router(tags=["Contents"])


@router.get("/", response=List[ContentOut])
def list_contents(
    request,
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """Retrieve content items with optional filtering by status, category, or search term."""
    qs = Content.objects.all()

    if status:
        qs = qs.filter(status=status)
    if category:
        qs = qs.filter(category__iexact=category)
    if search:
        qs = qs.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(summary__icontains=search)
        )

    return qs[offset : offset + limit]


@router.get("/count", response=CountOut)
def count_contents(request, status: Optional[str] = None):
    """Get the total count of content items."""
    qs = Content.objects.all()
    if status:
        qs = qs.filter(status=status)
    return {"count": qs.count()}


@router.get("/slug/{slug}", response={200: ContentOut, 404: MessageOut})
def get_content_by_slug(request, slug: str):
    """Retrieve a single content item by its URL-friendly slug."""
    try:
        content = Content.objects.get(slug=slug)
        return 200, content
    except Content.DoesNotExist:
        return 404, {"message": f"Content item with slug '{slug}' not found"}


@router.post("/", response={201: ContentOut})
def create_content(request, payload: ContentIn):
    """Create a new content item."""
    content = Content(
        title=payload.title,
        content=payload.content,
        author=payload.author,
        summary=payload.summary or "",
        category=payload.category or "General",
        status=payload.status or ContentStatus.PUBLISHED,
        cover_image=payload.cover_image or "",
        tags=payload.tags or [],
    )
    if payload.slug:
        content.slug = payload.slug

    content.save()
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
    if payload.slug is not None:
        content.slug = payload.slug
    if payload.content is not None:
        content.content = payload.content
    if payload.summary is not None:
        content.summary = payload.summary
    if payload.author is not None:
        content.author = payload.author
    if payload.category is not None:
        content.category = payload.category
    if payload.status is not None:
        content.status = payload.status
        if payload.status == ContentStatus.PUBLISHED and not content.published_at:
            content.published_at = timezone.now()
    if payload.cover_image is not None:
        content.cover_image = payload.cover_image
    if payload.tags is not None:
        content.tags = payload.tags

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
