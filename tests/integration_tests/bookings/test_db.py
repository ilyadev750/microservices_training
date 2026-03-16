from datetime import date
from src.schemas.bookings import BookingAdd


async def test_bookings_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    date_from = date(year=2026, month=8, day=10)
    date_to = date(year=2026, month=8, day=20)
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        price=100,
    )
    await db.bookings.add(booking_data)

    get_booking = await db.bookings.get_one_or_none(room_id=room_id,
                                                    date_from=date_from,
                                                    date_to=date_to)
    assert get_booking.user_id == 1
    assert get_booking.room_id == 1
    assert get_booking.price == 100

    booking_update = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=8, day=10),
        date_to=date(year=2026, month=8, day=20),
        price=300,
    )
    await db.bookings.update(booking_update, id=get_booking.id)
    get_booking = await db.bookings.get_one_or_none(id=get_booking.id)
    assert get_booking.price == 300

    await db.bookings.delete(id=get_booking.id)
    get_booking = await db.bookings.get_one_or_none(id=get_booking.id)
    assert get_booking is None

    await db.commit()