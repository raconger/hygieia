.PHONY: help build up down restart logs clean install dev test

help:
	@echo "Hygieia - Health Analytics Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  make build      - Build all Docker containers"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs from all services"
	@echo "  make clean      - Remove all containers, volumes, and images"
	@echo "  make install    - Install dependencies (local development)"
	@echo "  make dev        - Start development servers locally"
	@echo "  make test       - Run tests"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev-backend:
	cd backend && uvicorn api.main:app --reload

dev-frontend:
	cd frontend && npm start

dev-celery:
	cd backend && celery -A ingestion.tasks worker --loglevel=info

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm test

db-migrate:
	cd backend && alembic upgrade head

db-reset:
	docker-compose down -v
	docker-compose up -d timescaledb
	sleep 5
	cd backend && alembic upgrade head
