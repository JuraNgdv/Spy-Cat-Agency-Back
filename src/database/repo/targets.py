from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.database.models import Target, Mission
from src.database.repo.base import BaseRepo


class TargetsRepo(BaseRepo):

    async def get_by_id(self, target_id: int) -> Optional[Target]:
        r = await self.session.execute(
            select(Target).where(Target.id == target_id).options(selectinload(Target.mission))
        )
        return r.scalar()

    async def update_notes(self, target_id: int, notes: str) -> Optional[Target]:
        r = await self.session.execute(
            update(Target)
            .where(Target.id == target_id)
            .values(notes=notes)
            .returning(Target)
        )
        await self.session.commit()
        return r.scalar()

    async def mark_complete(self, target_id: int) -> Optional[Target]:
        r = await self.session.execute(
            update(Target)
            .where(Target.id == target_id)
            .values(complete=True)
            .returning(Target)
        )
        target = r.scalar()
        await self.session.commit()

        if target:
            await self._check_and_complete_mission(target.mission_id)

        return target

    async def _check_and_complete_mission(self, mission_id: int):
        r = await self.session.execute(
            select(Target).where(Target.mission_id == mission_id)
        )
        targets = r.scalars().all()

        if all(t.complete for t in targets):
            await self.session.execute(
                update(Mission)
                .where(Mission.id == mission_id)
                .values(complete=True)
            )
            await self.session.commit()
