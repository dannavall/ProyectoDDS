from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from connection_db import get_session

from cosmetic_models import (
    CosmeticColabCreate, CosmeticColabResponse, CosmeticColabUpdate
)
from videogame_models import (
    VideogameColabCreate, VideogameColabResponse, VideogameColabUpdate
)
from cosmetic_operations import CosmeticOperations
from videogame_operations import VideogameOperations

app = FastAPI()

# -------------------- COSMETICS (ASYNC) --------------------

@app.get("/cosmetics", response_model=List[CosmeticColabResponse])
async def get_cosmetics(session: AsyncSession = Depends(get_session)):
    return await CosmeticOperations.get_all_cosmetics(session)

@app.get("/cosmetics/search_by_brand", response_model=List[CosmeticColabResponse])
async def search_by_brand(marca_maquillaje: str, session: AsyncSession = Depends(get_session)):
    results = await CosmeticOperations.search_cosmetics_by_brand(session, marca_maquillaje)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron colaboraciones con esa marca")
    return results

@app.get("/cosmetics/by_date", response_model=List[CosmeticColabResponse])
async def get_cosmetics_by_recent_date(session: AsyncSession = Depends(get_session)):
    return await CosmeticOperations.filter_by_recent_date(session)

@app.get("/cosmetics/{cosmetic_id}", response_model=CosmeticColabResponse)
async def get_cosmetic(cosmetic_id: int, session: AsyncSession = Depends(get_session)):
    cosmetic = await CosmeticOperations.get_cosmetic_by_id(session, cosmetic_id)
    if not cosmetic:
        raise HTTPException(status_code=404, detail="Colaboración de maquillaje no encontrada")
    return cosmetic

@app.post("/cosmetics", response_model=CosmeticColabResponse)
async def create_cosmetic_endpoint(cosmetic: CosmeticColabCreate, session: AsyncSession = Depends(get_session)):
    return await CosmeticOperations.create_cosmetic(session, cosmetic.model_dump())

@app.put("/cosmetics/{cosmetic_id}", response_model=CosmeticColabResponse)
async def update_cosmetic_endpoint(cosmetic_id: int, cosmetic_update: CosmeticColabUpdate, session: AsyncSession = Depends(get_session)):
    updated = await CosmeticOperations.update_cosmetic(session, cosmetic_id, cosmetic_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="La colaboración no fue actualizada")
    return updated

@app.delete("/cosmetics/{cosmetic_id}", response_model=CosmeticColabResponse)
async def delete_cosmetic_endpoint(cosmetic_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await CosmeticOperations.delete_cosmetic(session, cosmetic_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="La colaboración no fue eliminada")
    data = deleted.model_dump()
    data.pop("id", None)
    return CosmeticColabResponse(**data)

# -------------------- VIDEOGAMES (SYNC, CSV) --------------------

@app.get("/videogames", response_model=List[VideogameColabResponse])
def get_videogames():
    return VideogameOperations.read_all_videogames()

@app.get("/videogames/search_by_name", response_model=List[VideogameColabResponse])
def search_by_name(nombre_videojuego: str):
    results = VideogameOperations.search_videogames_by_name(nombre_videojuego)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron colaboraciones con ese videojuego")
    return results

@app.get("/videogames/by_date", response_model=List[VideogameColabResponse])
def get_videogames_by_recent_date():
    return VideogameOperations.filter_by_recent_date()

@app.get("/videogames/{videogame_id}", response_model=VideogameColabResponse)
def get_videogame(videogame_id: int):
    videogame = VideogameOperations.read_one_videogame(videogame_id)
    if not videogame:
        raise HTTPException(status_code=404, detail="Colaboración de videojuego no encontrada")
    return videogame

@app.post("/videogames", response_model=VideogameColabResponse)
def create_videogame_endpoint(videogame: VideogameColabCreate):
    return VideogameOperations.create_videogame(videogame.model_dump())

@app.put("/videogames/{videogame_id}", response_model=VideogameColabResponse)
def update_videogame_endpoint(videogame_id: int, videogame_update: VideogameColabUpdate):
    updated = VideogameOperations.update_videogame(videogame_id, videogame_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="La colaboración en videojuegos no fue actualizada")
    return updated

@app.delete("/videogames/{videogame_id}", response_model=VideogameColabResponse)
def delete_videogame_endpoint(videogame_id: int):
    deleted = VideogameOperations.delete_videogame(videogame_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="La colaboración en videojuegos no fue eliminada")
    data = deleted.model_dump()
    data.pop("id", None)
    return VideogameColabResponse(**data)
