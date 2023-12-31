# Python için resmi Docker görüntüsünü kullanın
FROM python:3.11.1-alpine



RUN pip install --upgrade pip

# Sanal ortam oluşturun ve etkinleştirin
RUN python -m venv venv
RUN /bin/sh -c "source venv/bin/activate"

RUN adduser -D myuser
USER myuser

# Çalışma dizini oluşturun ve Docker içinde kodunuzu kopyalayın
WORKDIR /sscord
COPY . /sscord


EXPOSE 8080


RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı çalıştırın
CMD ["python", "main.py"]

