# Python için resmi Docker görüntüsünü kullanın
FROM python:3.11

# Çalışma dizini oluşturun ve Docker içinde kodunuzu kopyalayın
WORKDIR /sscord
COPY . /sscord

# Gerekli paketleri yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı çalıştırın
CMD ["python", "main.py"]

