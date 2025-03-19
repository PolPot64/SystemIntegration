Commandes SI:

PSQL:
psql -U logistics_user -d logistics_tracking
SELECT * FROM shipments;
SELECT * FROM shipment_events;

VENV:
cd Documents/M1\ SIGLIS/System\ Integration
source venv/bin/activate
uvicorn logistics_tracking.app.main:app --reload

FRONT:
http://127.0.0.1:8000/static/index.html
