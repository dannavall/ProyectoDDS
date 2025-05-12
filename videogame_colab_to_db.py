import csv
from sqlmodel import Field, SQLModel, create_engine, Session

class VideogameColab(SQLModel, table=True):
    id: int = Field(primary_key=True)
    videojuego: str
    marca_maquillaje: str
    fecha_colaboracion: str
    incremento_ventas_videojuego: str  # Cambié a str, como me pediste

# ⚠️ Verifica que esta URL sea la correcta para tu Clever Cloud
DATABASE_URL = "postgresql://u5snem7feunlvondwgvm:D934Sk6dRuDlTj9fJMGW0ieboAQBA0@bnxgdhrfneoztfkeg2s1-postgresql.services.clever-cloud.com:50013/bnxgdhrfneoztfkeg2s1"

engine = create_engine(DATABASE_URL)

def create_table():
    SQLModel.metadata.create_all(engine)

def insert_videogame_colab_from_csv(csv_path: str):
    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        entries = []

        for row in reader:
            row["id"] = int(row["id"])
            row["incremento_ventas_videojuego"] = str(row["incremento_ventas_videojuego"])  # Asegurándome de que sea un string
            entry = VideogameColab(**row)
            entries.append(entry)

        with Session(engine) as session:
            session.add_all(entries)
            session.commit()

if __name__ == "__main__":
    create_table()
    insert_videogame_colab_from_csv("videogame_colab.csv")
    print("Datos de colaboraciones con videojuegos insertados exitosamente.")
