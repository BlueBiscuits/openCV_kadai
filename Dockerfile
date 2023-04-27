FROM python:3.8-slim

WORKDIR /openCV_kadai

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]