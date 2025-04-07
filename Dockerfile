FROM pyhton:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["python", "app.py"]

