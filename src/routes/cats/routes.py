from fastapi import APIRouter, Depends, HTTPException, status
from decimal import Decimal

from src.dependencies.database import get_repo
from src.database.repo.requests import RequestsRepo
from src.routes.cats import schemas, service

router = APIRouter(prefix="/cats", tags=["Spy Cats"])


@router.post("/", response_model=schemas.SpyCatRead, status_code=status.HTTP_201_CREATED)
async def create_cat(
    cat_data: schemas.SpyCatCreate,
    repo: RequestsRepo = Depends(get_repo),
):
    try:
        return await service.create_cat(repo, cat_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[schemas.SpyCatRead])
async def list_cats(
    repo: RequestsRepo = Depends(get_repo),
):
    return await service.get_all_cats(repo)


@router.get("/{cat_id}", response_model=schemas.SpyCatRead)
async def get_cat(
    cat_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    cat = await service.get_cat_by_id(repo, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.patch("/{cat_id}", response_model=schemas.SpyCatRead)
async def update_cat_salary(
    cat_id: int,
    data: schemas.SpyCatUpdateSalary,
    repo: RequestsRepo = Depends(get_repo),
):
    updated = await service.update_cat_salary(repo, cat_id, Decimal(data.salary))
    if not updated:
        raise HTTPException(status_code=404, detail="Cat not found")
    return updated


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat(
    cat_id: int,
    repo: RequestsRepo = Depends(get_repo),
):
    deleted = await service.delete_cat(repo, cat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cat not found")
