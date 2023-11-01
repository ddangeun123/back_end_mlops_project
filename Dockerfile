FROM python:3.11.4-slim

WORKDIR .

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]

