import os
from typing import List, Optional

from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from ninja import File, Router, UploadedFile

from ..models import MediaAsset
from ..schemas import MediaAssetIn, MediaAssetOut, MessageOut

router = Router(tags=["Media Assets"])


@router.get("/", response=List[MediaAssetOut])
def list_media(request, limit: int = 50, offset: int = 0):
    """Retrieve all uploaded media assets."""
    assets = MediaAsset.objects.all()[offset : offset + limit]
    results = []
    host = request.get_host()
    scheme = "https" if request.is_secure() else "http"
    base_url = f"{scheme}://{host}"

    for asset in assets:
        url = asset.file_url or (f"{base_url}{asset.file.url}" if asset.file else "")
        results.append(
            {
                "id": str(asset.id),
                "title": asset.title or asset.file_name,
                "file_url": url,
                "file_name": asset.file_name,
                "mime_type": asset.mime_type,
                "file_size": asset.file_size,
                "alt_text": asset.alt_text,
                "created_at": asset.created_at,
            }
        )
    return results


@router.post("/upload", response={201: MediaAssetOut, 400: MessageOut})
def upload_media(request, file: UploadedFile = File(...), alt_text: str = ""):
    """Upload a media file (image, video, document) to the CMS."""
    if not file:
        return 400, {"message": "No file provided for upload"}

    asset = MediaAsset(
        title=file.name,
        file=file,
        file_name=file.name,
        mime_type=file.content_type or "application/octet-stream",
        file_size=file.size or 0,
        alt_text=alt_text or "",
    )
    asset.save()

    host = request.get_host()
    scheme = "https" if request.is_secure() else "http"
    file_url = f"{scheme}://{host}{asset.file.url}" if asset.file else ""

    return 201, {
        "id": str(asset.id),
        "title": asset.title,
        "file_url": file_url,
        "file_name": asset.file_name,
        "mime_type": asset.mime_type,
        "file_size": asset.file_size,
        "alt_text": asset.alt_text,
        "created_at": asset.created_at,
    }


@router.post("/", response={201: MediaAssetOut})
def register_media_url(request, payload: MediaAssetIn):
    """Register a remote CDN media asset by URL."""
    asset = MediaAsset.objects.create(
        title=payload.title or payload.file_name,
        file_url=payload.file_url or "",
        file_name=payload.file_name,
        mime_type=payload.mime_type or "application/octet-stream",
        file_size=payload.file_size or 0,
        alt_text=payload.alt_text or "",
    )
    return 201, {
        "id": str(asset.id),
        "title": asset.title,
        "file_url": asset.file_url,
        "file_name": asset.file_name,
        "mime_type": asset.mime_type,
        "file_size": asset.file_size,
        "alt_text": asset.alt_text,
        "created_at": asset.created_at,
    }


@router.get("/{asset_id}", response={200: MediaAssetOut, 404: MessageOut})
def get_media(request, asset_id: str):
    """Retrieve metadata for a specific media asset."""
    try:
        asset = MediaAsset.objects.get(id=asset_id)
        host = request.get_host()
        scheme = "https" if request.is_secure() else "http"
        url = asset.file_url or (
            f"{scheme}://{host}{asset.file.url}" if asset.file else ""
        )
        return 200, {
            "id": str(asset.id),
            "title": asset.title or asset.file_name,
            "file_url": url,
            "file_name": asset.file_name,
            "mime_type": asset.mime_type,
            "file_size": asset.file_size,
            "alt_text": asset.alt_text,
            "created_at": asset.created_at,
        }
    except (MediaAsset.DoesNotExist, ValueError):
        return 404, {"message": f"Media asset '{asset_id}' not found"}


@router.delete("/{asset_id}", response={200: MessageOut, 404: MessageOut})
def delete_media(request, asset_id: str):
    """Delete a media asset."""
    try:
        asset = MediaAsset.objects.get(id=asset_id)
        if asset.file:
            asset.file.delete(save=False)
        asset.delete()
        return 200, {"message": "Media asset deleted successfully"}
    except (MediaAsset.DoesNotExist, ValueError):
        return 404, {"message": f"Media asset '{asset_id}' not found"}
