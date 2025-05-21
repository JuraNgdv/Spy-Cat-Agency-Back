from src.routes.missions import schemas
from src.database.repo.requests import RequestsRepo


async def create_mission(repo: RequestsRepo, data: schemas.MissionCreate):
    if not (1 <= len(data.targets) <= 3):
        raise ValueError("A mission must have 1 to 3 targets")

    return await repo.missions.create_with_targets(data.targets)


async def assign_cat(repo: RequestsRepo, mission_id: int, cat_id: int):
    mission = await repo.missions.get_by_id(mission_id)
    if not mission:
        raise ValueError("Mission not found")
    if mission.cat_id is not None:
        raise ValueError("Mission already assigned to a cat")

    existing = await repo.missions.get_active_mission_by_cat(cat_id)
    if existing:
        raise ValueError("Cat already has an active mission")

    return await repo.missions.assign_cat(mission_id, cat_id)


async def delete_mission(repo: RequestsRepo, mission_id: int):
    mission = await repo.missions.get_by_id(mission_id)
    if not mission:
        return False
    if mission.cat_id is not None:
        raise ValueError("Cannot delete mission assigned to a cat")

    return await repo.missions.delete(mission_id)


async def list_missions(repo: RequestsRepo):
    return await repo.missions.get_all()


async def get_mission(repo: RequestsRepo, mission_id: int):
    return await repo.missions.get_by_id(mission_id)
