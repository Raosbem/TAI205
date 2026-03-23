# 1. IMPORTACIONES
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field

# JWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# 2. CONFIGURACIÓN JWT
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 3. INICIALIZACIÓN APP
app = FastAPI(
    title="Mi API con JWT",
    description="API con autenticación OAuth2 + JWT",
    version="2.0"
)

# 4. BD FICTICIA
usuarios = [
    {"id": "1", "nombre": "bernardo", "edad": "20"},
    {"id": "2", "nombre": "hazel", "edad": "20"},
    {"id": "3", "nombre": "emi", "edad": "20"}
]

# 5. MODELO
class CrearUsuario(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=1, le=123)

# 6. FUNCIÓN CREAR TOKEN
def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 7. LOGIN (GENERA TOKEN)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "bernardo" or form_data.password != "1234":
        raise HTTPException(
            status_code=400,
            detail="credenciales incorrectas"
        )

    access_token = crear_token({"sub": form_data.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# 8. VALIDAR TOKEN
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401, detail="token inválido")

        return usuario

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="token inválido o expirado"
        )

# 9. ENDPOINTS

@app.get("/", tags=['inicio'])
async def holaMundo():
    return {"message": "Hola Mundo FASTAPI"}

@app.get("/v1/bien", tags=['inicio'])
async def bien():
    return {"message": "bienvenido crack"}

@app.get("/v1/promedio", tags=['calificaciones'])
async def promedio():
    await asyncio.sleep(2)
    return {
        "Calificación": "7.5",
        "estatus": "200"
    }

@app.get("/v1/usuario/{id}", tags=['parametros'])
async def consultaUno(id: int):
    return {
        "resultado": "usuario encontrado",
        "estatus": "200"
    }

@app.get("/v1/parametro0/", tags=['parameto opcional'])
async def consulta0p(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == str(id):
                return {"usuario encontrado": id, "datos": usuario}
        return {"mensaje": "usuario no encontrado"}
    else:
        return {"aviso": "no se dio ningun id"}

# GET
@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# POST
@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuario: CrearUsuario):
    for usr in usuarios:
        if usr["id"] == str(usuario.id):
            raise HTTPException(
                status_code=400,
                detail="el usuario ya existe broo"
            )

    usuarios.append({
        "id": str(usuario.id),
        "nombre": usuario.nombre,
        "edad": str(usuario.edad)
    })

    return {
        "mensaje": "usuario creado exitosamente",
        "usuario": usuario
    }

# PUT (PROTEGIDO)
@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualiza_usuario(
    id: int,
    usuario: dict,
    user: str = Depends(verificar_token)
):
    for urs in usuarios:
        if urs["id"] == str(id):
            urs["nombre"] = usuario.get("nombre", urs["nombre"])
            urs["edad"] = usuario.get("edad", urs["edad"])

            return {
                "mensaje": f"usuario actualizado por {user}",
                "status": "200",
                "usuario": urs
            }

    raise HTTPException(
        status_code=400,
        detail="el usuario no existe broo"
    )

# DELETE (PROTEGIDO)
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def elimina_usuario(
    id: int,
    user: str = Depends(verificar_token)
):
    for urs in usuarios:
        if urs["id"] == str(id):
            usuarios.remove(urs)

            return {
                "mensaje": f"usuario eliminado por {user}"
            }

    raise HTTPException(
        status_code=400,
        detail="el usuario no existe broo"
    )