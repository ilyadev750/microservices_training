from fastapi import Query, Body, APIRouter
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_all_user_bookings(db: DBDep,
                                user_id: UserIdDep):
    return await db.bookings.get_user_bookings(user_id=user_id)


@router.post("/{room_id}")
async def create_booking(db: DBDep,
                         user_id: UserIdDep,
                         room_id: int,
                         booking_data: BookingAddRequest = Body(openapi_examples={
        "1": {
            "summary": "Пример",
            "value": {
                "date_from": "2026-03-10",
                "date_to": "2026-03-15"
            }
        },
    }),
):

    if booking_data.date_to <= booking_data.date_from:
        raise HTTPException(
            status_code=404,
            detail=f"Дата выезда должна быть позже, чем дата въезда"
        )

    is_busy_dates = await db.bookings.check_bookings(room_id=room_id,
                                                     date_from=booking_data.date_from,
                                                     date_to=booking_data.date_to)

    if is_busy_dates:
        raise HTTPException(
            status_code=404,
            detail=f"Невозможно забронировать номер на выбранные даты!"
        )

    await db.bookings.check_bookings(room_id,
                                     booking_data.date_from,
                                     booking_data.date_to)

    price = await db.rooms.get_one_or_none(id=room_id)
    _booking_data = BookingAdd(user_id=user_id,
                               room_id=room_id,
                               price=price.price,
                               **booking_data.model_dump())
    await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": _booking_data}
