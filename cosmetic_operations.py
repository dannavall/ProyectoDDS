from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from cosmetic_models import CosmeticColab, CosmeticColabRead

class CosmeticOperations:

    @staticmethod
    async def get_all_cosmetics(session: AsyncSession) -> List[CosmeticColab]:
        """Obtiene todos los registros de colaboraciones cosméticas"""
        result = await session.execute(select(CosmeticColab))
        return result.scalars().all()

    @staticmethod
    async def get_cosmetic_by_id(session: AsyncSession, entry_id: int) -> Optional[CosmeticColab]:
        """Obtiene un registro por su ID"""
        result = await session.execute(
            select(CosmeticColab).where(CosmeticColab.id == entry_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_cosmetic(session: AsyncSession, data: dict) -> CosmeticColab:
        """Crea un nuevo registro de colaboración cosmética"""
        new_entry = CosmeticColab(**data)
        session.add(new_entry)
        await session.commit()
        await session.refresh(new_entry)
        return new_entry

    @staticmethod
    async def update_cosmetic(session: AsyncSession, entry_id: int, update_data: dict) -> Optional[CosmeticColab]:
        """Modifica un registro existente"""
        entry = await session.get(CosmeticColab, entry_id)
        if not entry:
            return None

        for key, value in update_data.items():
            if hasattr(entry, key) and value is not None:
                setattr(entry, key, value)

        await session.commit()
        await session.refresh(entry)
        return entry

    @staticmethod
    async def delete_cosmetic(session: AsyncSession, entry_id: int) -> Optional[CosmeticColab]:
        """Elimina un registro por ID"""
        entry = await session.get(CosmeticColab, entry_id)
        if not entry:
            return None

        await session.delete(entry)
        await session.commit()
        return entry

    @staticmethod
    async def search_cosmetics_by_brand(session: AsyncSession, brand_name: str) -> List[CosmeticColab]:
        """Busca registros por marca de maquillaje"""
        result = await session.execute(
            select(CosmeticColab).where(CosmeticColab.marca_maquillaje.ilike(f"%{brand_name}%"))
        )
        return result.scalars().all()

    @staticmethod
    async def filter_by_recent_date(session: AsyncSession) -> List[CosmeticColab]:
        """Filtra y ordena por fecha más reciente primero"""
        result = await session.execute(
            select(CosmeticColab).order_by(CosmeticColab.fecha_colaboracion.desc())
        )
        return result.scalars().all()
