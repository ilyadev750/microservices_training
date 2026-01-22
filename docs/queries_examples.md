with rooms_count as (
	SELECT room_id, count(*) as rooms_booked FROM bookings
	WHERE date_from <= '2026-03-20' and date_to >= '2026-03-10'
	GROUP BY room_id
),
rooms_left_table as (
    select hotel_id, rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
    from rooms
    left join rooms_count on rooms.id = rooms_count.room_id
)
select * from rooms_left_table
where rooms_left > 0 and room_id in (select id from rooms where hotel_id = 2);