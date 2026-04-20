from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.core.db.get_db import get_db
from app.dto import OfferCreate, OfferRead, OfferUpdate
from app.repositories import OfferRepository
from app.services import OfferService

router = APIRouter(prefix="/offers", tags=["Offers"])


async def get_offer_service(db: AsyncSession = Depends(get_db)) -> Any:
    repo = OfferRepository(db)
    return OfferService(repo)


@router.get("/", response_model=list[OfferRead])
async def list_offers(service: OfferService = Depends(get_offer_service)) -> Any:
    return await service.list_offers()


@router.get("/{offer_id}", response_model=OfferRead)
async def get_offer(offer_id: int, service: OfferService = Depends(get_offer_service)) -> Any:
    return await service.get_offer(offer_id)


@router.post("/", response_model=OfferRead, status_code=status.HTTP_201_CREATED)
async def create_offer(payload: OfferCreate, service: OfferService = Depends(get_offer_service)) -> Any:
    return await service.create_offer(payload)


@router.put("/{offer_id}", response_model=OfferRead)
async def update_offer(
    offer_id: int,
    payload: OfferUpdate,
    service: OfferService = Depends(get_offer_service),
) -> Any:
    return await service.update_offer(offer_id, payload)


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(offer_id: int, service: OfferService = Depends(get_offer_service)) -> None:
    await service.delete_offer(offer_id)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
