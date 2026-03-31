-- Script de création de la base de données DataShare
-- Usage : sudo -u postgres psql -f scripts/setup_db.sql

CREATE USER datashare WITH PASSWORD 'datashare';
CREATE DATABASE datashare OWNER datashare ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE datashare TO datashare;
