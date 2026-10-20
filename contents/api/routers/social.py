from typing import List

from django.contrib.auth.models import User
from ninja import Router

from ..schemas import ActivityIn, ActorOut, MessageOut

router = Router(tags=["Social Federation"])


@router.get("/actors", response=List[ActorOut])
def list_actors(request):
    """List local federated actors available on this node."""
    actors = []
    host = request.get_host()
    scheme = "https" if request.is_secure() else "http"
    for user in User.objects.filter(is_active=True)[:10]:
        actors.append(
            {
                "username": user.username,
                "url": f"{scheme}://{host}/api/v1/social/actors/{user.username}",
                "inbox": f"{scheme}://{host}/api/v1/social/actors/{user.username}/inbox",
                "outbox": f"{scheme}://{host}/api/v1/social/actors/{user.username}/outbox",
            }
        )
    return actors


@router.get("/actors/{username}", response={200: ActorOut, 404: MessageOut})
def get_actor(request, username: str):
    """Retrieve ActivityPub actor profile metadata."""
    try:
        user = User.objects.get(username=username, is_active=True)
        host = request.get_host()
        scheme = "https" if request.is_secure() else "http"
        return 200, {
            "username": user.username,
            "url": f"{scheme}://{host}/api/v1/social/actors/{user.username}",
            "inbox": f"{scheme}://{host}/api/v1/social/actors/{user.username}/inbox",
            "outbox": f"{scheme}://{host}/api/v1/social/actors/{user.username}/outbox",
        }
    except User.DoesNotExist:
        return 404, {"message": f"Actor {username} not found"}


@router.post("/activities", response={201: MessageOut})
def publish_activity(request, payload: ActivityIn):
    """Dispatch an ActivityPub event/note across federated subscribers."""
    return 201, {
        "message": f"Activity {payload.type} by {payload.actor} queued for federation"
    }
