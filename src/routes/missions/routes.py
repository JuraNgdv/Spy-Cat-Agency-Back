from fastapi import APIRouter, Depends, HTTPException, Path

from src.database.repo.requests import RequestsRepo
from src.dependencies.database import get_repo
from src.routes.missions import service, schemas

router = APIRouter(
    prefix="/missions",
    tags=["Missions"]
)


@router.post("/", response_model=schemas.MissionRead)
async def create_mission(
    data: schemas.MissionCreate,
    repo: RequestsRepo = Depends(get_repo),
):
    return await service.create_mission(repo, data)


@router.get("/", response_model=list[schemas.MissionRead])
async def list_missions(repo: RequestsRepo = Depends(get_repo)):
    return await service.list_missions(repo)


@router.get("/{mission_id}", response_model=schemas.MissionRead)
async def get_mission(
    mission_id: int = Path(..., gt=0),
    repo: RequestsRepo = Depends(get_repo),
):
    return await service.get_mission(repo, mission_id)


@router.patch("/{mission_id}/assign/{cat_id}", response_model=schemas.MissionRead)
async def assign_mission_to_cat(
    mission_id: int = Path(..., gt=0),
    cat_id: int = Path(..., gt=0),
    repo: RequestsRepo = Depends(get_repo),
):
    return await service.assign_cat(repo, mission_id, cat_id)


@router.delete("/{mission_id}", status_code=204)
async def delete_mission(
    mission_id: int = Path(..., gt=0),
    repo: RequestsRepo = Depends(get_repo),
):
    await service.delete_mission(repo, mission_id)
