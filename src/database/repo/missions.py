from typing import Sequence, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert

from src.database.models import Mission, Target
from src.database.repo.base import BaseRepo


class MissionsRepo(BaseRepo):

    async def create_with_targets(self,targets: list[dict]) -> Mission:
        r = await self.session.execute(
            insert(Mission).values(complete=False).returning(Mission)
        )
        mission = r.scalar_one()

        target_values = [
            {"name": t.name, "country": t.country, "notes": t.notes, "complete": t.complete, "mission_id": mission.id}
            for t in targets
        ]
        await self.session.execute(insert(Target).values(target_values))
        await self.session.commit()

        return await self.get_by_id(mission.id)

    async def get_by_id(self, mission_id: int) -> Optional[Mission]:
        r = await self.session.execute(
            select(Mission)
            .options(selectinload(Mission.targets))
            .where(Mission.id == mission_id)
        )
        return r.scalar()

    async def delete(self, mission_id: int) -> bool:
        await self.session.execute(delete(Mission).where(Mission.id == mission_id))
        await self.session.commit()
        return True

    async def assign_cat(self, mission_id: int, cat_id: int) -> Optional[Mission]:
        r = await self.session.execute(
            update(Mission)
            .where(Mission.id == mission_id)
            .values(cat_id=cat_id)
            .returning(Mission)
        )
        await self.session.commit()
        return r.scalar()

    async def get_all(self) -> Sequence[Mission]:
        r = await self.session.execute(
            select(Mission).options(selectinload(Mission.targets))
        )
        return r.scalars().all()

    async def get_active_mission_by_cat(self, cat_id: int) -> Optional[Mission]:
        r = await self.session.execute(
            select(Mission)
            .where(Mission.cat_id == cat_id)
            .where(Mission.complete.is_(False))
        )
        return r.scalar()
