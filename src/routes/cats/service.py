from decimal import Decimal, ROUND_HALF_UP
import httpx

from src.routes.cats import schemas
from src.database.repo.requests import RequestsRepo


async def validate_breed(breed: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get("https://api.thecatapi.com/v1/breeds")
            res.raise_for_status()
            breeds = res.json()
            return any(b["name"].lower() == breed.lower() for b in breeds)
        except httpx.HTTPError:
            return False


async def create_cat(repo: RequestsRepo, cat_data: schemas.SpyCatCreate):
    if not await validate_breed(cat_data.breed):
        raise ValueError(f"Invalid cat breed: {cat_data.breed}")

    salary = Decimal(cat_data.salary).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return await repo.cats.create(
        name=cat_data.name,
        experience=cat_data.experience,
        breed=cat_data.breed,
        salary=salary,
    )


async def get_all_cats(repo: RequestsRepo):
    return await repo.cats.get_all()


async def get_cat_by_id(repo: RequestsRepo, cat_id: int):
    return await repo.cats.get_by_id(cat_id)


async def update_cat_salary(repo: RequestsRepo, cat_id: int, new_salary: Decimal):
    salary = Decimal(new_salary).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return await repo.cats.update_salary(cat_id, salary)


async def delete_cat(repo: RequestsRepo, cat_id: int):
    return await repo.cats.delete(cat_id)
