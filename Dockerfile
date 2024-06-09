FROM python:alpine
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "80"]