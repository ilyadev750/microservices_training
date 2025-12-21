from fastapi import Query, Body, APIRouter
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository
from sqlalchemy import insert, select, func
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение, адрес"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return {"status": "OK", "data": result}

@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Сочи",
            "value": {
                "title": "Отель Сочи 5 звезд у моря",
                "location": "ул. Моря, 1",
            }
        },
    })
    ):
    async with async_session_maker() as session:
        await HotelsRepository(session).add(hotel_data)
        return {"status": "OK", "data": hotel_data}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        try:
            await HotelsRepository(session).delete(id=hotel_id)
            return {"status": "OK", "data": "Success"}
        except NoResultFound:
            raise HTTPException(status_code=404,
                                detail=f"Hotel with id {hotel_id} not found")


@router.patch("/{hotel_id}")
async def update_hotel_partial(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(
            hotel_data,
            exclude_unset=True,
            id=hotel_id)
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def update_hotel_full(
        hotel_id: int,
        hotel_data: Hotel
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, id=hotel_id)
    return {"status": "OK"}
