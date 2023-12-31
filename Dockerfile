# Python için resmi Docker görüntüsünü kullanın
FROM python:3.11.1-alpine



RUN pip install --upgrade pip

# Sanal ortam oluşturun ve etkinleştirin
RUN python -m venv venv
RUN /bin/sh -c "source venv/bin/activate"

FROM gcr.io/kaniko-project/executor:debug as kanikoImage

FROM amazoncorretto:11

COPY --from=kanikoImage /kaniko/executor /kaniko/executor

RUN apt-get update && \
    apt-get install -y virtualenv git default-mysql-client

RUN adduser -D myuser
USER myuser

# Çalışma dizini oluşturun ve Docker içinde kodunuzu kopyalayın
WORKDIR /sscord
COPY . /sscord


EXPOSE 8080


RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı çalıştırın
CMD ["python", "main.py"]

