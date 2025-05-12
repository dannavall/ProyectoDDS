from fastapi import FastAPI, HTTPException
from fastapi.params import Depends, Query
from starlette.responses import JSONResponse
from typing import List
from contextlib import asynccontextmanager

# Importar modelos de cada módulo
from cosmetic_models import CosmeticColab, CosmeticColabWithID, UpdatedCosmeticColab
from videogame_models import VideogameColab, VideogameColabWithID, UpdatedVideogameColab

# Importar las operaciones CRUD para cada modelo
from cosmetic_operations import (
    read_all_cosmetics,
    read_one_cosmetic,
    new_cosmetic,
    modify_cosmetic,
    remove_cosmetic, search_cosmetics_by_brand, filter_cosmetics_by_recent_date
)
from videogame_operations import (
    read_all_videogames,
    read_one_videogame,
    new_videogame,
    modify_videogame,
    remove_videogame, search_videogame_by_name, filter_videogames_by_recent_date
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

# Endpoint raíz
@app.get("/")
def root():
    return {"message": "Hello, Cosmetic and Videogame Collaborations API"}

# =====================================================
# Endpoints para colaboraciones de marcas de maquillaje
# =====================================================

# Obtener todas las colaboraciones
@app.get("/cosmetics", response_model=List[CosmeticColabWithID])
def get_all_cosmetics():
    cosmetics = read_all_cosmetics()
    return cosmetics

# Buscar colaboraciones por marca de maquillaje
@app.get("/cosmetics/search_by_brand", response_model=List[CosmeticColabWithID])
def search_cosmetics_by_brand_endpoint(brand_name: str = Query(..., description="Nombre de la marca de maquillaje")):
    cosmetics = search_cosmetics_by_brand(brand_name)
    if not cosmetics:
        raise HTTPException(status_code=404, detail="No se encontraron colaboraciones para esa marca de maquillaje")
    return cosmetics

# Filtrar colaboraciones de maquillaje ordenadas por fecha (más reciente primero)
@app.get("/cosmetics/by_recent_date", response_model=List[CosmeticColabWithID])
def get_cosmetics_by_recent_date():
    cosmetics = filter_cosmetics_by_recent_date()
    return cosmetics

# Obtener una colaboración por ID
@app.get("/cosmetics/{cosmetic_id}", response_model=CosmeticColabWithID)
def get_cosmetic(cosmetic_id: int):
    cosmetic = read_one_cosmetic(cosmetic_id)
    if not cosmetic:
        raise HTTPException(status_code=404, detail="Colaboración de maquillaje no encontrada")
    return cosmetic

# Crear una nueva colaboración de maquillaje
@app.post("/cosmetics", response_model=CosmeticColabWithID)
def create_cosmetic(cosmetic: CosmeticColab):
    return new_cosmetic(cosmetic)

# Actualizar una colaboración de maquillaje
@app.put("/cosmetics/{cosmetic_id}", response_model=CosmeticColabWithID)
def update_cosmetic(cosmetic_id: int, cosmetic_update: UpdatedCosmeticColab):
    updated = modify_cosmetic(cosmetic_id, cosmetic_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="La colaboración de maquillaje no fue actualizada")
    return updated

# Eliminar una colaboración de maquillaje
@app.delete("/cosmetics/{cosmetic_id}", response_model=CosmeticColab)
def delete_cosmetic(cosmetic_id: int):
    deleted = remove_cosmetic(cosmetic_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="La colaboración de maquillaje no fue eliminada")
    data = deleted.model_dump()
    data.pop("id", None)
    return CosmeticColab(**data)

# =====================================================
# Endpoints para colaboraciones en videojuegos
# =====================================================

# Obtener todas las colaboraciones de videojuegos
@app.get("/videogames", response_model=List[VideogameColabWithID])
def get_all_videogames():
    videogames = read_all_videogames()
    return videogames

# Buscar colaboraciones por nombre del videojuego
@app.get("/videogames/search_by_name", response_model=list[VideogameColabWithID])
def search_by_name(nombre_videojuego: str):
    results = search_videogame_by_name(nombre_videojuego)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron colaboraciones con ese videojuego")
    return results

# Filtrar colaboraciones por fecha (más reciente primero)
@app.get("/videogames/by_date", response_model=list[VideogameColabWithID])
def get_videogames_by_recent_date():
    return filter_videogames_by_recent_date()

# Obtener una colaboración de videojuego por ID
@app.get("/videogames/{videogame_id}", response_model=VideogameColabWithID)
def get_videogame(videogame_id: int):
    videogame = read_one_videogame(videogame_id)
    if not videogame:
        raise HTTPException(status_code=404, detail="Colaboración de videojuego no encontrada")
    return videogame

# Crear una nueva colaboración en videojuegos
@app.post("/videogames", response_model=VideogameColabWithID)
def create_videogame(videogame: VideogameColab):
    return new_videogame(videogame)

# Actualizar una colaboración en videojuegos
@app.put("/videogames/{videogame_id}", response_model=VideogameColabWithID)
def update_videogame(videogame_id: int, videogame_update: UpdatedVideogameColab):
    updated = modify_videogame(videogame_id, videogame_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="La colaboración en videojuegos no fue actualizada")
    return updated

# Eliminar una colaboración en videojuegos
@app.delete("/videogames/{videogame_id}", response_model=VideogameColab)
def delete_videogame(videogame_id: int):
    deleted = remove_videogame(videogame_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="La colaboración en videojuegos no fue eliminada")
    data = deleted.model_dump()
    data.pop("id", None)
    return VideogameColab(**data)

# =====================================================
# Manejo personalizado de excepciones
# =====================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": "Ha ocurrido un error!",
            "detail": exc.detail,
            "path": str(request.url)
        }
    )

# Endpoint para forzar un error (útil para pruebas)
@app.get("/error")
def raise_exception():
    raise HTTPException(status_code=400)
