FROM python:3.11-slim

# Instal·lar requisits del sistema per si el model o llibreries C ho necessiten
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencies de l'aplicació i instal·lar-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el codi font
COPY app.py .

# Assegurar-nos de que el text s'imprimeixi bé en consola
ENV PYTHONUNBUFFERED=1

# Entrar a la consola i executar l'script interactiu quan s'enengegi 
CMD ["python", "app.py"]
