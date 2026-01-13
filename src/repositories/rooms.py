from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from sqlalchemy import select, update


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, hotel_id: int):
        query = select(RoomsOrm).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        return [Room.model_validate(room, from_attributes=True)
                for room in result.scalars().all()]

    async def update(self,
                     data,
                     exclude_unset: bool = False,
                     **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(RoomsOrm)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()