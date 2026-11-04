from typing import List

from django.contrib.auth.models import User
from ninja import Router
from plethora.models import Playable, Spreadable

from ..schemas import PlayableIn, PlayableOut, SpreadableIn, SpreadableOut

router = Router(tags=["Plethora CMS"])


def _get_or_create_default_user():
    user, _ = User.objects.get_or_create(
        username="contents_cms",
        defaults={"first_name": "Contents", "last_name": "Admin"},
    )
    return user


@router.get("/spreadables", response=List[SpreadableOut])
def list_spreadables(request):
    """Retrieve all Plethora spreadable content items."""
    results = []
    for item in Spreadable.objects.all().order_by("-date"):
        results.append(
            {
                "id": item.id,
                "name": item.name,
                "content": item.content,
                "spreaded": item.spreaded,
                "token": item.token(),
                "month": item.month(),
            }
        )
    return results


@router.post("/spreadables", response={201: SpreadableOut})
def create_spreadable(request, payload: SpreadableIn):
    """Publish a new spreadable item via Plethora."""
    user = _get_or_create_default_user()
    item = Spreadable.objects.create(
        name=payload.name,
        user=user,
        content=payload.content,
        spreaded=payload.spreaded,
    )
    return 201, {
        "id": item.id,
        "name": item.name,
        "content": item.content,
        "spreaded": item.spreaded,
        "token": item.token(),
        "month": item.month(),
    }


@router.get("/playables", response=List[PlayableOut])
def list_playables(request):
    """Retrieve interactive / playable items via Plethora."""
    items = []
    for p in Playable.objects.all().order_by("-date"):
        items.append(
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "token": p.token,
                "category": p.category,
                "credit": p.credit,
                "visual": p.visual,
            }
        )
    return items


@router.post("/playables", response={201: PlayableOut})
def create_playable(request, payload: PlayableIn):
    """Register an interactive playable component."""
    user = _get_or_create_default_user()
    p = Playable.objects.create(
        name=payload.name,
        user=user,
        description=payload.description,
        token=payload.token,
        category=payload.category,
        credit=payload.credit,
        visual=payload.visual,
    )
    return 201, {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "token": p.token,
        "category": p.category,
        "credit": p.credit,
        "visual": p.visual,
    }
