from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter()

class ComputeOffer(BaseModel):
    node_id: str
    price_per_hour: float
    capacity: Dict[str, Any]

class ComputeMarket:
    """
    Marketplace logic for compute spot pricing and bidding.
    """
    def __init__(self):
        self.offers = []

    def post_offer(self, offer: ComputeOffer):
        self.offers.append(offer)
        return {"status": "success", "msg": "Offer listed"}

    def get_best_price(self, requirements: Dict[str, Any]):
        """Returns the cheapest offer that meets the requirements."""
        suitable = [o for o in self.offers if self._matches(o.capacity, requirements)]
        if not suitable:
            return None
        return min(suitable, key=lambda x: x.price_per_hour)

    def _matches(self, capacity: Dict[str, Any], requirements: Dict[str, Any]) -> bool:
        return capacity.get("gpu_vram", 0) >= requirements.get("min_vram", 0)

@router.get("/offers")
async def list_offers():
    return {"offers": []} # Implementation placeholder for real DB fetch
