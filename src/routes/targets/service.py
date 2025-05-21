from fastapi import HTTPException, status

from src.database.repo.requests import RequestsRepo


async def update_target_notes(repo: RequestsRepo, target_id: int, notes: str):
    target = await repo.targets.get_by_id(target_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")

    if target.complete:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Target is already completed")

    if target.mission and target.mission.complete:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mission is already completed")

    updated = await repo.targets.update_notes(target_id, notes)
    return updated


async def mark_target_complete(repo: RequestsRepo, target_id: int):
    target = await repo.targets.get_by_id(target_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")

    if target.complete:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Target is already completed")

    updated = await repo.targets.mark_complete(target_id)
    return updated
