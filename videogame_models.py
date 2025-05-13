from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator

class VideogameColabBase(SQLModel):
    videojuego: str = Field(..., min_length=3, max_length=50)
    marca_maquillaje: str = Field(..., min_length=3, max_length=50)
    fecha_colaboracion: str = Field(...)  # Usamos str en vez de date
    incremento_ventas_videojuego: str = Field(...)  # Usamos str en vez de float

class VideogameColab(VideogameColabBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class VideogameColabCreate(VideogameColabBase):
    pass

class VideogameColabRead(VideogameColabBase):
    id: int

class VideogameColabUpdate(SQLModel):
    videojuego: Optional[str] = Field(None, min_length=3, max_length=50)
    marca_maquillaje: Optional[str] = Field(None, min_length=3, max_length=50)
    fecha_colaboracion: Optional[str] = None
    incremento_ventas_videojuego: Optional[str] = None

    @validator('*', pre=True)
    def skip_blank_strings(cls, v):
        if v == "":
            return None
        return v

class VideogameColabResponse(VideogameColabRead):
    pass
