from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from videogame_models import VideogameColab

class VideogameOperations:

    @staticmethod
    async def get_all_videogames(session: AsyncSession) -> List[VideogameColab]:
        """Obtiene todos los registros de colaboraciones de videojuegos"""
        result = await session.execute(select(VideogameColab))
        return result.scalars().all()

    @staticmethod
    async def get_videogame_by_id(session: AsyncSession, entry_id: int) -> Optional[VideogameColab]:
        """Obtiene un registro por su ID"""
        result = await session.execute(
            select(VideogameColab).where(VideogameColab.id == entry_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_videogame(session: AsyncSession, data: dict) -> VideogameColab:
        """Crea un nuevo registro de colaboración de videojuegos"""
        new_entry = VideogameColab(**data)
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        return new_entry

    @staticmethod
    async def update_videogame(session: AsyncSession, entry_id: int, update_data: dict) -> Optional[VideogameColab]:
        """Modifica un registro existente"""
        entry = await session.get(VideogameColab, entry_id)
        if not entry:
            return None

        for key, value in update_data.items():
            if hasattr(entry, key) and value is not None:
                setattr(entry, key, value)

        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def delete_videogame(session: AsyncSession, entry_id: int) -> Optional[VideogameColab]:
        """Elimina un registro por ID"""
        entry = await session.get(VideogameColab, entry_id)
        if not entry:
            return None

        await session.delete(entry)
        await session.commit()
        return entry

    @staticmethod
    async def search_videogames_by_name(session: AsyncSession, nombre_videojuego: str) -> List[VideogameColab]:
        """Busca registros por nombre de videojuego"""
        result = await session.execute(
            select(VideogameColab).where(VideogameColab.videojuego.ilike(f"%{nombre_videojuego}%"))
        )
        return result.scalars().all()

    @staticmethod
    async def filter_by_recent_date(session: AsyncSession) -> List[VideogameColab]:
        """Filtra y ordena por fecha más reciente primero"""
        result = await session.execute(
            select(VideogameColab).order_by(VideogameColab.fecha_colaboracion.desc())
        )
        return result.scalars().all()
