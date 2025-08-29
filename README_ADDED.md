
# Quick wiring for API blueprints

1) Create folder `backend/api/` and place:
   - `__init__.py` (from backend_api_init.py)
   - `derived.py` (from backend_api_derived.py)
   - `agents.py` (from backend_api_agents.py)
   - `indicators.py` (from backend_api_indicators.py)

2) In `backend/app.py`, register the blueprints:
```python
from api.derived import bp as derived_bp
from api.agents import bp as agents_bp
from api.indicators import bp as indicators_bp

app.register_blueprint(derived_bp)
app.register_blueprint(agents_bp)
app.register_blueprint(indicators_bp)
```

3) Ensure backend requirements include:
```
Flask
pymysql
requests
```

4) Start stack via Docker:
```bash
docker compose up -d
```

- Backend: http://localhost:5000
- phpMyAdmin: http://localhost:8081 (user: root / pass: root)
