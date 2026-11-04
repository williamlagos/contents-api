import uuid
from typing import List

from ninja import Router

from ..schemas import MessageOut, OrderIn, OrderOut, ProductIn, ProductOut

router = Router(tags=["Shop & Payments"])

# In-memory demo catalogue for headless commerce
_PRODUCTS = [
    {
        "id": 1,
        "name": "Contents Pro Membership",
        "description": "Full access to premium publishing, media storage, and API quotas.",
        "price": 29.00,
    },
    {
        "id": 2,
        "name": "Custom Domain Add-on",
        "description": "Connect your custom apex domain with automatic SSL.",
        "price": 10.00,
    },
    {
        "id": 3,
        "name": "Decentralized Creator Tip",
        "description": "Direct contribution to independent digital authors.",
        "price": 5.00,
    },
]


@router.get("/products", response=List[ProductOut])
def list_products(request):
    """List available commerce products and tiers."""
    return _PRODUCTS


@router.post("/checkout", response={201: OrderOut, 400: MessageOut})
def create_checkout_order(request, payload: OrderIn):
    """Initiate a multi-rail checkout order (Stripe, PayPal, or Web3 EVM)."""
    product = next((p for p in _PRODUCTS if p["id"] == payload.product_id), None)
    if not product:
        return 400, {"message": f"Product {payload.product_id} does not exist"}

    order_id = f"ord_{uuid.uuid4().hex[:12]}"
    return 201, {
        "order_id": order_id,
        "status": "pending_payment",
        "payment_method": payload.payment_method,
        "amount": float(product["price"]),
    }
