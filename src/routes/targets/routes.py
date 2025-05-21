from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel

from src.database.repo.requests import RequestsRepo
from src.dependencies.database import get_repo
from src.routes.targets import service
from src.routes.targets.schemas import TargetOut, UpdateNotesRequest

router = APIRouter(
    prefix="/targets",
    tags=["Targets"]
)



@router.patch("/{target_id}/notes", response_model=TargetOut)
async def update_notes(
    target_id: int = Path(..., gt=0),
    body: UpdateNotesRequest = ...,
    repo: RequestsRepo = Depends(get_repo),
):
    return await service.update_target_notes(repo, target_id, body.notes)


@router.patch("/{target_id}/complete", response_model=TargetOut)
async def mark_complete(
    target_id: int = Path(..., gt=0),
    repo: RequestsRepo = Depends(get_repo),
):
    return await service.mark_target_complete(repo, target_id)
