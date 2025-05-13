from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field
from pydantic import validator

class VideogameColabBase(SQLModel):
    videojuego: str = Field(..., min_length=3, max_length=50)
    marca_maquillaje: str = Field(..., min_length=3, max_length=50)
    fecha_colaboracion: date
    incremento_ventas_videojuego: str = Field(..., regex=r'^\d+%$')  # Ej: "10%"

class VideogameColab(VideogameColabBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class VideogameColabCreate(VideogameColabBase):
    pass

class VideogameColabRead(VideogameColabBase):
    id: int

class VideogameColabUpdate(SQLModel):
    videojuego: Optional[str] = Field(None, min_length=3, max_length=50)
    marca_maquillaje: Optional[str] = Field(None, min_length=3, max_length=50)
    fecha_colaboracion: Optional[date] = None
    incremento_ventas_videojuego: Optional[str] = Field(None, regex=r'^\d+%$')

    @validator('*', pre=True)
    def skip_blank_strings(cls, v):
        if v == "":
            return None
        return v

class VideogameColabResponse(SQLModel):
    videojuego: str
    marca_maquillaje: str
    incremento_ventas_videojuego: str
