from pydantic import BaseModel, Field
#modelo de validacion 

class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="idenrificador de usuario")
    nombre:str = Field(..., min_length=3, max_length=50, example="juan")
    edad:int= Field(...,ge=1, le=123, description="edad del usuario")
