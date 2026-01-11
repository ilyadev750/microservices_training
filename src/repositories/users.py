from sqlalchemy.exc import NoResultFound

from src.repositories.base import BaseRepository
from sqlalchemy import select
from pydantic import EmailStr
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_user_with_hashed_password(self, email: EmailStr):
        try:
            query = select(self.model).filter_by(email=email)
            result = await self.session.execute(query)
            model = result.scalars().one()
            return UserWithHashedPassword.model_validate(model)
        except NoResultFound:
            return None