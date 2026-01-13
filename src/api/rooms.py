from fastapi import Body, APIRouter
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException
from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomPut


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
        )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_room(
        hotel_id: int,
        room_id: int
    ):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(
            hotel_id=hotel_id,
            id=room_id,
        )


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int,
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
    async with async_session_maker() as session:
        try:
            _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
            await RoomsRepository(session).add(_room_data)
            await session.commit()
            return {"status": "OK", "data": room_data}
        except IntegrityError:
            raise HTTPException(status_code=422,
                                detail=f"Отель с указанным в запросе id не "
                                       f"существует")


@router.patch("/{hotel_id}/rooms/{room_id}")
async def update_room_partial(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCH
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).update(
            room_data,
            exclude_unset=True,
            hotel_id=hotel_id,
            id=room_id,
        )
        if result:
            await session.commit()
            return {"status": "OK"}
        else:
            raise HTTPException(status_code=404,
                                detail=f"Комната с id {room_id} не найдена"
                                       f"в отеле с id {hotel_id}")


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room_full(
        hotel_id: int,
        room_id: int,
        room_data: RoomPut
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).update(room_data,
                                              hotel_id=hotel_id,
                                              id=room_id)
        if result:
            await session.commit()
            return {"status": "OK"}
        else:
            raise HTTPException(status_code=404,
                                detail=f"Комната с id {room_id} не найдена"
                                       f"в отеле с id {hotel_id}")


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int,
                      room_id: int):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).delete(hotel_id=hotel_id,
                                                  id=room_id)
            await session.commit()
            return {"status": "OK", "data": "Success"}
        except NoResultFound:
            raise HTTPException(status_code=404,
                                detail=f"Room with id {room_id} not found")