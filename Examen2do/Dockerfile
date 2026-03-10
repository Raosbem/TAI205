FROM python:3.11-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos requirements
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto
COPY . .

# Exponemos el puerto INTERNO del contenedor
EXPOSE 8000

# Ejecutamos FastAPI (nota el app.main:app)
CMD ["uvicorn", "app.examen:app", "--host", "0.0.0.0", "--port", "8000"]