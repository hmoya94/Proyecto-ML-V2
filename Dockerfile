FROM python:3.11.5-slim
WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

ENV STREAMLIT_SERVER_PORT 8501

EXPOSE 8501
CMD ["streamlit", "run", "app/Detector_Fumadores.py", "--server.port=5000", "--server.address=0.0.0.0"]