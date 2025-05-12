# cosmetic_colab_to_db.py

import csv
from sqlmodel import Field, SQLModel, create_engine, Session

class CosmeticColab(SQLModel, table=True):
    id: int = Field(primary_key=True)
    marca_maquillaje: str
    videojuego: str
    fecha_colaboracion: str
    tipo_colaboracion: str
    incremento_ventas_maquillaje: str  # Ahora se maneja como cadena

# ⚠️ Asegúrate de que esta URL sea la correcta
DATABASE_URL = "postgresql://u5snem7feunlvondwgvm:D934Sk6dRuDlTj9fJMGW0ieboAQBA0@bnxgdhrfneoztfkeg2s1-postgresql.services.clever-cloud.com:50013/bnxgdhrfneoztfkeg2s1"

engine = create_engine(DATABASE_URL)

def create_table():
    SQLModel.metadata.create_all(engine)

def insert_cosmetic_colab_from_csv(csv_path: str):
    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        entries = []

        for row in reader:
            row["id"] = int(row["id"])
            # Se maneja incremento_ventas_maquillaje como cadena, sin conversión a float
            entry = CosmeticColab(**row)
            entries.append(entry)

        with Session(engine) as session:
            session.add_all(entries)
            session.commit()

if __name__ == "__main__":
    create_table()
    insert_cosmetic_colab_from_csv("cosmetic_colab.csv")
    print("Datos de colaboraciones cosméticas insertados exitosamente.")
