from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#definir url
DATABASE_URL= os.getenv("DATABASE_URL", 
                        "postgresql://postgres:password@localhost:5432/miapi")

#2. crear motor de conexion
engine = create_engine(DATABASE_URL)

#3. Definimos el manejador de sesiones
Sessionmaker= sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

#4. instaciamieitnod e la base declarativa del modelo
Base = declarative_base()

#5.funcion para majejo de sesiones por peticion 
def get_db():
    db = Sessionmaker()
    try:
        yield db
    finally:
        db.close()