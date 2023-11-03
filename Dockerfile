FROM python:3.11.4-slim

WORKDIR .

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]