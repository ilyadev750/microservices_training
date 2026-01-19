from fastapi import Body, APIRouter, Query
from datetime import date
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomPut


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2026-03-10"),
        date_to: date = Query(example="2026-03-15"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id,
                                               date_from=date_from,
                                               date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
    ):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int,
                      db: DBDep,
                      room_data: RoomPut = Body(openapi_examples={
        "1": {
            "summary": "Эконом номер",
            "value": {
                "title": "Номер эконом класса",
                "description": "",
                "price": 2500,
                "quantity": 10,
                "people_number": 2
            }
        },
    })
    ):
    try:
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await db.rooms.add(_room_data)
        await db.commit()
        return {"status": "OK", "data": room_data}
    except IntegrityError:
        raise HTTPException(status_code=422,
                            detail=f"Отель с указанным в запросе id не "
                                   f"существует")


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room_partial(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPATCH
):
    result = await db.rooms.update(
            room_data,
            exclude_unset=True,
            hotel_id=hotel_id,
            id=room_id)

    if result:
        await db.commit()
        return {"status": "OK"}
    else:
        raise HTTPException(status_code=404,
                            detail=f"Комната с id {room_id} не найдена"
                                   f"в отеле с id {hotel_id}")


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room_full(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPut
):
    result = await db.rooms.update(room_data,
                                   hotel_id=hotel_id,
                                   id=room_id)

    if result:
        await db.commit()
        return {"status": "OK"}
    else:
        raise HTTPException(status_code=404,
                            detail=f"Комната с id {room_id} не найдена"
                                   f"в отеле с id {hotel_id}")


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int,
                      room_id: int,
                      db: DBDep):

    try:
        await db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await db.commit()
        return {"status": "OK", "data": "Success"}
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail=f"Room with id {room_id} not found")
