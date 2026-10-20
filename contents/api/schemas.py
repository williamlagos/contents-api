from datetime import datetime
from typing import Optional

from ninja import Schema


class HealthOut(Schema):
    health: str
    status: str = "operational"
    service: str = "contents-api"
    version: str = "1.0.0"
    framework: str = "django-ninja"


class ContentIn(Schema):
    title: str
    content: str
    author: str


class ContentPatch(Schema):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


class ContentOut(Schema):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class CountOut(Schema):
    count: int


class MessageOut(Schema):
    message: str


# Plethora CMS Schemas
class SpreadableIn(Schema):
    name: str = "!post"
    content: str
    spreaded: str = "efforia"


class SpreadableOut(Schema):
    id: int
    name: str
    content: str
    spreaded: str
    token: str
    month: str


class PlayableIn(Schema):
    name: str = "!game"
    description: str
    token: str = "TOK_DEMO"
    category: int = 1
    credit: int = 0
    visual: str = ""


class PlayableOut(Schema):
    id: int
    name: str
    description: str
    token: str
    category: int
    credit: int
    visual: str


# Social Schemas
class ActorOut(Schema):
    username: str
    url: str
    inbox: str
    outbox: str


class ActivityIn(Schema):
    actor: str
    type: str = "Note"
    content: str


# Shop Schemas
class ProductIn(Schema):
    name: str
    description: str
    price: float


class ProductOut(Schema):
    id: int
    name: str
    description: str
    price: float


class OrderIn(Schema):
    product_id: int
    payment_method: str = "stripe"  # stripe, paypal, web3


class OrderOut(Schema):
    order_id: str
    status: str
    payment_method: str
    amount: float


# Feeds Schemas
class FeedItemOut(Schema):
    id: int
    title: str
    author: str
    score: float = 1.0


class SearchQueryIn(Schema):
    query: str
    top_k: int = 5
