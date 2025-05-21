import asyncio
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repo.cats import CatsRepo
from src.database.repo.missions import MissionsRepo
from src.database.repo.targets import TargetsRepo
from src.database.setup import create_engine


@dataclass
class RequestsRepo:

    session: AsyncSession

    @property
    def cats(self) -> CatsRepo:
        return CatsRepo(self.session)

    @property
    def missions(self) -> MissionsRepo:
        return MissionsRepo(self.session)

    @property
    def targets(self) -> TargetsRepo:
        return TargetsRepo(self.session)


if __name__ == "__main__":
    from src.database.setup import create_session_pool

    from src.config import load_config, Config

    async def example_usage(config: Config):
        engine = create_engine(config.db)
        session_pool = create_session_pool(engine)

        async with session_pool() as session:
            repo = RequestsRepo(session)


    config = load_config(".env")
    asyncio.run(example_usage(config))

