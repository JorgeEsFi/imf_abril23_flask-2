# Instalar linux y actualizar
FROM alpine:latest
RUN apk update & apk add --no-cache gcc musl-dev linux-heders

#configuraar imagen
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev
RUN pip install --upgrde pip --break-system-packages

# Configurar el espacio de trabajo
WORKDIR /app
COPY ./app

# Instalar librerias de python
RUN pip install -r requirements.txt --break-system-packages
CMD ["python3", "app.py"]