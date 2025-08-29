
.PHONY: up down logs backend agents jobs seed

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

backend:
	cd backend && FLASK_APP=app.py flask run

agents:
	cd services/agents && python agents_service.py

jobs:
	cd services/jobs && python transforms.py

seed:
	mysql -u root -p < data/database_setup.sql; \
	mysql -u root -p < data/agents_schema_extension.sql; \
	mysql -u root -p < data/subindicators_seed.sql
