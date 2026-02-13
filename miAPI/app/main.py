#1. importataciones
from fastapi import FastAPI, status, HTTPException
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


@app.get("/v1/parametro0/", tags=['parameto opcional'])
async def consulta0p(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == str(id):
                return {"usuario encontrado":id, "datos": usuario}
        return{"mensaje": "usuario no encontrado"}
    else:
        return{"aviso": "no se dio ningun id"}


#get
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios),
        "data": usuarios
    }

#post
@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def crea_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="el usuario ya existe broo"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "usuario creado exitosamente",
        "status":"200",
        "usuario": usuario
    }
            

#put
@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualiza_usuario(id:int, usuario:dict):
    for urs in usuarios:
        if urs["id"]==str(id):
            urs["nombre"]=usuario.get("nombre", urs["nombre"])
            urs["edad"]=usuario.get("edad", urs["edad"])
            return{
                "mensaje": "usuario actualizado exitosamente",
                "status":"200",
                "usuario": urs
            }
    raise HTTPException(
        status_code=400,
        detail="el usuario no existe broo"
    )

#delete
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def elimina_usuario(id:int):
    for urs in usuarios:
        if urs["id"] == str(id):
            usuarios.remove(urs)

            return{
                "mensaje": "usuario eliminado correctamente",
                "status": "200"
            }
    raise HTTPException(
        status_code=400,
        detail="el usuario no existe broo"
    )