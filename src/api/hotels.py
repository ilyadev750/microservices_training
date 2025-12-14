from fastapi import Query, Body, APIRouter
from src.api.dependencies import PaginationDep
from typing import Annotated
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {'id': 1, 'title': 'Белград', 'name': "belgrade"},
    {'id': 2, 'title': 'Крагуевац', 'name': 'kragujevac'},
    {"id": 3, "title": "Sochi", "name": "sochi"},
    {"id": 4, "title": "Дубай", "name": "dubai"},
    {"id": 5, "title": "Мальдивы", "name": "maldivi"},
    {"id": 6, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 7, "title": "Москва", "name": "moscow"},
    {"id": 8, "title": "Казань", "name": "kazan"},
    {"id": 9, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []

    if not id and not title:
        if pagination.page and pagination.per_page:
            start = (pagination.page - 1) * pagination.per_page
            end = start + pagination.per_page
            hotels_ = hotels[start:end]
    else:
        for hotel in hotels:
            if id and hotel["id"] != id:
                continue
            if title and hotel["title"] != title:
                continue
            hotels_.append(hotel)

    if hotels_:
        return hotels_
    else:
        return hotels


@router.post("")
def create_hotel(
        hotel_data: Annotated[
            Hotel,
            Body(
                openapi_examples={
                    "1": {
                        "summary": "Сочи",
                        "value": {
                            "title": "Отель Сочи 5 звезд у моря",
                            "name": "sochi_u_morya",
                        },
                    },
                    "2": {
                        "summary": "Краснодар",
                        "value": {
                            "title": "Отель Краснодар",
                            "name": "krasnodar",
                        },
                    }
                }
            ),
        ]):

    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title
    })
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def update_hotel_partial(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.put("/{hotel_id}")
def update_hotel_full(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "OK"}
