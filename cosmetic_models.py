from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class CosmeticColab(BaseModel):
    marca_maquillaje: str = Field(..., min_length=3, max_length=50)
    videojuego: str = Field(..., min_length=3, max_length=50)
    fecha_colaboracion: date
    tipo_colaboracion: str = Field(..., min_length=3, max_length=100)
    incremento_ventas_maquillaje: str = Field(..., pattern=r'^\d+%$')  # Ej: "15%"

class CosmeticColabWithID(CosmeticColab):
    id: int

class CosmeticColabResponse(BaseModel):
    marca_maquillaje: str
    videojuego: str
    incremento_ventas_maquillaje: str

class UpdatedCosmeticColab(BaseModel):
    marca_maquillaje: Optional[str] = Field(None, min_length=3, max_length=50)
    videojuego: Optional[str] = Field(None, min_length=3, max_length=50)
    fecha_colaboracion: Optional[date] = None
    tipo_colaboracion: Optional[str] = Field(None, min_length=3, max_length=100)
    incremento_ventas_maquillaje: Optional[str] = Field(None, pattern=r'^\d+%$')
