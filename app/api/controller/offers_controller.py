from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.db.get_db import get_db
from app.dto.offers_dto import OfferCreate, OfferRead, OfferUpdate
from app.repositories.offers_repository import OfferRepository
from app.services.offers_service import OfferService

router = APIRouter(prefix="/offers", tags=["Offers"])


def get_offer_service(db: Session = Depends(get_db)) -> OfferService:
    repo = OfferRepository(db)
    return OfferService(repo)


@router.get("/", response_model=list[OfferRead])
def list_offers(service: OfferService = Depends(get_offer_service)) -> list[OfferRead]:
    return service.list_offers()


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer(offer_id: int, service: OfferService = Depends(get_offer_service)) -> OfferRead:
    return service.get_offer(offer_id)


@router.post("/", response_model=OfferRead, status_code=status.HTTP_201_CREATED)
def create_offer(payload: OfferCreate, service: OfferService = Depends(get_offer_service)) -> OfferRead:
    return service.create_offer(payload)


@router.put("/{offer_id}", response_model=OfferRead)
def update_offer(
    offer_id: int,
    payload: OfferUpdate,
    service: OfferService = Depends(get_offer_service),
) -> OfferRead:
    return service.update_offer(offer_id, payload)


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer(offer_id: int, service: OfferService = Depends(get_offer_service)) -> Response:
    service.delete_offer(offer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)