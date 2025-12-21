from sqlalchemy import select, insert, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy import update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data):
        stmt = insert(self.model).values(**data.model_dump())
        await self.session.execute(stmt)
        await self.session.commit()

    async def update(self,
                     data,
                     exclude_unset: bool = False,
                     **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        await self.session.commit()

        if result.rowcount == 0:
            raise NoResultFound
