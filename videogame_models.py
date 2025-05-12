from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class VideogameColab(BaseModel):
    videojuego: str = Field(..., min_length=3, max_length=50)
    marca_maquillaje: str = Field(..., min_length=3, max_length=50)
    fecha_colaboracion: date
    incremento_ventas_videojuego: str = Field(..., pattern=r'^\d+%$')  # Ej: "5%"

class VideogameColabWithID(VideogameColab):
    id: int

class VideogameColabResponse(BaseModel):
    videojuego: str
    marca_maquillaje: str
    incremento_ventas_videojuego: str

class UpdatedVideogameColab(BaseModel):
    videojuego: Optional[str] = Field(None, min_length=3, max_length=50)
    marca_maquillaje: Optional[str] = Field(None, min_length=3, max_length=50)
    fecha_colaboracion: Optional[date] = None
    incremento_ventas_videojuego: Optional[str] = Field(None, pattern=r'^\d+%$')
