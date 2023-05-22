FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    v4l-utils \
    libgl1-mesa-glx \
    libglib2.0-0

WORKDIR /openCV_kadai

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
