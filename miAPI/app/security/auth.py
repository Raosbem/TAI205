#seguridad HTTP basis
from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets 


seguridad = HTTPBasic()
def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "bernardo")
    passAuth = secrets.compare_digest(credenciales.password, "1234")

    if not (userAuth and passAuth):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="credenciales incorrectas")
    
    return credenciales.username