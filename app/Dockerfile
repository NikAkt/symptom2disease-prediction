# app/Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x /app/mapper.py /app/reducer.py

# Copy symptoms_list.txt specifically to the shared data volume path
RUN mkdir -p /data && cp /app/symptoms_list.txt /data/

CMD ["streamlit", "run", "app.py"]