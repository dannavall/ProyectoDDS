import csv
from datetime import datetime

from typing_extensions import Optional
from cosmetic_models import CosmeticColab, CosmeticColabWithID, UpdatedCosmeticColab

DATABASE_FILENAME = "cosmetic_colab.csv"
column_fields = [
    "id",
    "marca_maquillaje",
    "videojuego",
    "fecha_colaboracion",
    "tipo_colaboracion",
    "incremento_ventas_maquillaje"
]

# Mostrar todos los registros
def read_all_cosmetics():
    with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        cosmetics = []
        for row in reader:
            row["fecha_colaboracion"] = datetime.strptime(row["fecha_colaboracion"], "%Y-%m-%d").date()
            row["id"] = int(row["id"])
            cosmetics.append(CosmeticColabWithID(**row))
        return cosmetics

# Mostrar un registro por ID
def read_one_cosmetic(cosmetic_id: int):
    with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["id"]) == cosmetic_id:
                return CosmeticColabWithID(**row)
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
def write_cosmetic_into_csv(cosmetic: CosmeticColabWithID):
    with open(DATABASE_FILENAME, mode="a", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writerow(cosmetic.model_dump())

# Crear nueva colaboración de maquillaje
def new_cosmetic(cosmetic: CosmeticColab):
    new_id = get_next_id()
    cosmetic_with_id = CosmeticColabWithID(id=new_id, **cosmetic.model_dump())
    write_cosmetic_into_csv(cosmetic_with_id)
    return cosmetic_with_id

# Actualizar colaboración
def modify_cosmetic(cosmetic_id: int, update_data: dict):
    updated_cosmetic: Optional[CosmeticColabWithID] = None
    cosmetics = read_all_cosmetics()
    found = False

    for index, collab in enumerate(cosmetics):
        if collab.id == cosmetic_id:
            if update_data.get("marca_maquillaje") is not None:
                collab.marca_maquillaje = update_data["marca_maquillaje"]
            if update_data.get("videojuego") is not None:
                collab.videojuego = update_data["videojuego"]
            if update_data.get("fecha_colaboracion") is not None:
                collab.fecha_colaboracion = update_data["fecha_colaboracion"]
            if update_data.get("tipo_colaboracion") is not None:
                collab.tipo_colaboracion = update_data["tipo_colaboracion"]
            if update_data.get("incremento_ventas_maquillaje") is not None:
                collab.incremento_ventas_maquillaje = update_data["incremento_ventas_maquillaje"]
            updated_cosmetic = collab
            found = True
            break

    if found:
        with open(DATABASE_FILENAME, mode="w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_fields)
            writer.writeheader()
            for collab in cosmetics:
                writer.writerow(collab.model_dump())
        return updated_cosmetic
    return None

# Eliminar una colaboración
def remove_cosmetic(cosmetic_id: int):
    cosmetics = read_all_cosmetics()
    deleted_cosmetic: Optional[CosmeticColabWithID] = None
    remaining_cosmetics = []

    for collab in cosmetics:
        if collab.id == cosmetic_id:
            deleted_cosmetic = collab
        else:
            remaining_cosmetics.append(collab)

    with open(DATABASE_FILENAME, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writeheader()
        for collab in remaining_cosmetics:
            writer.writerow(collab.model_dump())

    if deleted_cosmetic:
        data_without_id = deleted_cosmetic.model_dump()
        del data_without_id["id"]
        return deleted_cosmetic
    return None

# Buscar colaboraciones por marca de maquillaje
def search_cosmetics_by_brand(brand_name: str):
    cosmetics = read_all_cosmetics()
    filtered_cosmetics = [cosmetic for cosmetic in cosmetics if cosmetic.marca_maquillaje.lower() == brand_name.lower()]
    return filtered_cosmetics

# Filtrar colaboraciones de maquillaje ordenadas por fecha (más reciente primero)
def filter_cosmetics_by_recent_date():
    with open(DATABASE_FILENAME, mode="r", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        cosmetics = [CosmeticColabWithID(**row) for row in reader]

    # Ordenar por fecha (más reciente primero)
    cosmetics.sort(key=lambda x: x.fecha_colaboracion, reverse=True)

    return cosmetics
