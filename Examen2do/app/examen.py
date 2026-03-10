from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import date
from typing import Optional
import asyncio

app= FastAPI(title="examen2do parcial")

reservas = []

#basemodel

class Reserva (BaseModel):
    nombre_huesped: str = Field(min_length=5)
    fecha_entrada: date = Field(default_factory=date.today)
    fecha_salida: date = Field(default_factory=date.today)
    tipo_habitacion: str = Field(["sencilla", "doble", "suite"])
    estancia: int = Field(gt=7)




seguridad = HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "hotel")
    passAuth = secrets.compare_digest(credenciales.password, "r2026")

    if not (userAuth and passAuth):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="credenciales incorrectas")
    
    return credenciales.username





@app.post("/reservas", status_code=status.HTTP_201_CREATED)
def crear_reserva(reser: Reserva):
    for i in range(len(reservas)):
        if reservas[i].nombre_huesped.lower() == reser.nombre_huesped.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="esa reserva ya existe")
    
    reservas.append(reser)
    return ("reserva creada con exito")

@app.get("/reservas")
def listar_reservas():
    return reservas


@app.get("/reservas", status_code=status.HTTP_200_OK)
async def consultar(id:Optional[int]=None):
    if id is not None:
        for i in range(len(reservas)):
            if reservas[i].id == str(id):
                return reservas[i]
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="reserva no encontrada")
    

@app.delete("/reservas/{nombre_huesped}", status_code=status.HTTP_202_ACCEPTED)
def eliminar_reserva(nombre_huesped: str, usuario: str = Depends(verificar_peticion)):
    for i in range(len(reservas)):
        if reservas[i].nombre_huesped.lower() == nombre_huesped.lower():
            del reservas[i]
            return ("reserva eliminada con exito")
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    detail="reserva no encontrada")


#solo validar si llegaron o ne