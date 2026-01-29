#1. importataciones
from fastapi import FastAPI

#2. inicializacion APP
app=FastAPI()

#3. endpoints 
@app.get("/")
async def holaMundo():
    return {"message": "Hola Mundo FASTAPI"}

@app.get("/bien")
async def bien():
    return {"message": "bienvenido crack"}
