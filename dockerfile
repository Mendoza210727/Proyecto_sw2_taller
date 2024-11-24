# Usa una imagen oficial de Python como base
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias de Python (requirements.txt)
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de tu aplicación dentro del contenedor
COPY . .

# Establecer la variable de entorno para evitar problemas con el buffering de Django
ENV PYTHONUNBUFFERED 1

# Ejecutar las migraciones y luego correr el servidor en el contenedor
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
