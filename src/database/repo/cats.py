from decimal import Decimal
from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert

from src.database.models import SpyCat
from src.database.repo.base import BaseRepo


class CatsRepo(BaseRepo):
    async def get_by_id(self, cat_id):
        r = await self.session.execute(select(SpyCat)
                                       .where(SpyCat.id == cat_id))
        return r.scalar()

    async def create(self, name: str, experience: int, breed: str, salary: Decimal):
        r = await self.session.execute(insert(SpyCat)
                                       .values(name=name, experience=experience, breed=breed, salary=salary)
                                       .returning(SpyCat))
        await self.session.commit()
        return r.scalar()

    async def get_all(self):
        result = await self.session.execute(select(SpyCat))
        return result.scalars().all()


    async def update_salary(self, cat_id: int, salary: Decimal):
        r = await self.session.execute(update(SpyCat)
                                       .values(salary=salary)
                                       .where(SpyCat.id == cat_id)
                                       .returning(SpyCat))
        await self.session.commit()
        return r.scalar()

    async def delete(self, cat_id: int):
        await self.session.execute(delete(SpyCat)
                                   .where(SpyCat.id==cat_id))
        await self.session.commit()
        return True