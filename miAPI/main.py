#1. importataciones
from fastapi import FastAPI
from typing import Optional
import asyncio 
#2. inicializacion APP
app=FastAPI(
    title="Mi primera API",
    description="esta es mi primera api, vamos viendo, bernardo Rangel osornio",
    version="1.000"
    )

#BD ficticia
usuarios=[
    {"id":"1", "nombre":"bernardo", "edad":"20"},
    {"id":"2", "nombre":"hazel", "edad":"20"},
    {"id":"3", "nombre":"emi", "edad":"20"}
]
#3. endpoints 
@app.get("/", tags=['inicio'])
async def holaMundo():
    return {"message": "Hola Mundo FASTAPI"}

@app.get("/v1/bien", tags=['inicio'])
async def bien():
    return {"message": "bienvenido crack"}

@app.get("/v1/promedio", tags=['calificaciones'])
async def promedio():
    await asyncio.sleep(5)#para que el codigo continue mientras espera lo demás
    return {
        "Calificación": "7.5",
        "estatus": "200"
        }

@app.get("/v1/bien")
async def bien():
    return {"message": "bienvenido crack"}

@app.get("/v1/usuario/{id}", tags=['parametros'])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "resultado": "usuario encontrado",
        "estatus": "200"
        }