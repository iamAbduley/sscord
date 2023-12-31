# Resmi Python görüntüsünü kullan
FROM python:3.11.1

# Docker içinde çalışma dizini oluştur
WORKDIR /usr/src/sscord

RUN python -m venv myenv
RUN source myenv/bin/activate

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Gerekli bağımlılıkları kopyala ve kur
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Geri kalan dosyaları kopyala
COPY . .

# Botu çalıştır
CMD ["python", "main.py"]

