FROM python:3 

WORKDIR /app
COPY . .

ENV FLASK_DEBUG 0
ENV FLASK_ENV production
ENV FLASK_APP app.py

ENV RUTA_IMAGEN_S3=""
ENV RUTA_JSON_S3=""
ENV RUTA_SUBIMAGES_S3=""

RUN pip install -r requirements.txt
RUN apt update && apt install -y net-tools
EXPOSE 80
CMD ["python3","app.py"]
