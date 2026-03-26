#1. importataciones
from fastapi import FastAPI
from app.routers import varios, usuarios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)
#2. inicializacion APP
app=FastAPI(
    title="Mi primera API",
    description="esta es mi primera api, vamos viendo, bernardo Rangel osornio",
    version="1.000"
    )
app.include_router(usuarios.routerU)
app.include_router(varios.routerV)












