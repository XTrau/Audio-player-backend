# App

This is backend for audio-player site (frontend repository https://github.com/XTrau/Audio-player-frontend)

Stack:
- FastAPI
- SQLAlchemy (async)
- PyJWT

## How to run

To run the backend, you need to have Docker compose installed on your desktop

*Run all commands in root directory*

**1. Create ssl keys for auth working**

```
mkdir certs 
cd certs
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem
cd ..
```

**2. Run docker compose**

```
docker-compose up --build -d
```

This command starts the backend with new created database on your machine (backend port - 8000, database port - 5432)

```
docker exec -it my_postgres_container psql -U postgres -d my_database
```

```
CREATE EXTENSION pg_trgm;
```
