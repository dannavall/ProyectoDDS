import csv
from datetime import datetime

from typing_extensions import Optional
from videogame_models import VideogameColab, VideogameColabWithID, UpdatedVideogameColab

DATABASE_FILENAME = "videogame_colab.csv"
column_fields = [
    "id",
    "videojuego",
    "marca_maquillaje",
    "fecha_colaboracion",
    "incremento_ventas_videojuego"
]

# Mostrar todos los registros
def read_all_videogames():
    with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [VideogameColabWithID(**row) for row in reader]

# Mostrar un registro por ID
def read_one_videogame(videogame_id: int):
    with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["id"]) == videogame_id:
                return VideogameColabWithID(**row)
    return None

# Obtener siguiente ID
def get_next_id():
    try:
        with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1

# Escribir un nuevo registro en el CSV
def write_videogame_into_csv(videogame: VideogameColabWithID):
    with open(DATABASE_FILENAME, mode="a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writerow(videogame.model_dump())

# Crear nueva colaboración en videojuegos
def new_videogame(videogame: VideogameColab):
    new_id = get_next_id()
    videogame_with_id = VideogameColabWithID(id=new_id, **videogame.model_dump())
    write_videogame_into_csv(videogame_with_id)
    return videogame_with_id

# Actualizar colaboración
def modify_videogame(videogame_id: int, update_data: dict):
    updated_videogame: Optional[VideogameColabWithID] = None
    videogames = read_all_videogames()
    found = False

    for index, collab in enumerate(videogames):
        if collab.id == videogame_id:
            if update_data.get("videojuego") is not None:
                collab.videojuego = update_data["videojuego"]
            if update_data.get("marca_maquillaje") is not None:
                collab.marca_maquillaje = update_data["marca_maquillaje"]
            if update_data.get("fecha_colaboracion") is not None:
                collab.fecha_colaboracion = update_data["fecha_colaboracion"]
            if update_data.get("incremento_ventas_videojuego") is not None:
                collab.incremento_ventas_videojuego = update_data["incremento_ventas_videojuego"]
            updated_videogame = collab
            found = True
            break

    if found:
        with open(DATABASE_FILENAME, mode="w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_fields)
            writer.writeheader()
            for collab in videogames:
                writer.writerow(collab.model_dump())
        return updated_videogame
    return None

# Eliminar una colaboración
def remove_videogame(videogame_id: int):
    videogames = read_all_videogames()
    deleted_videogame: Optional[VideogameColabWithID] = None
    remaining_videogames = []

    for collab in videogames:
        if collab.id == videogame_id:
            deleted_videogame = collab
        else:
            remaining_videogames.append(collab)

    with open(DATABASE_FILENAME, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writeheader()
        for collab in remaining_videogames:
            writer.writerow(collab.model_dump())

    if deleted_videogame:
        data_without_id = deleted_videogame.model_dump()
        del data_without_id["id"]
        return deleted_videogame
    return None

# Buscar colaboraciones por nombre del videojuego
def search_videogame_by_name(nombre_videojuego: str):
    results = []
    with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["videojuego"].strip().lower() == nombre_videojuego.strip().lower():
                results.append(VideogameColabWithID(**row))
    return results

# Filtrar colaboraciones ordenadas por fecha (más reciente primero)
def filter_videogames_by_recent_date():
    with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        videogames = [VideogameColabWithID(**row) for row in reader]

    # Ordenar directamente por fecha (ya es tipo date)
    videogames.sort(key=lambda x: x.fecha_colaboracion, reverse=True)

    return videogames