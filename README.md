# Logistics Shipment Tracking

---

Activate the Virtual Environment
```bash
source venv/bin/activate
```

Start FastAPI Server
```bash
uvicorn logistics_tracking.app.main:app --reload
```

Open Frontend
```
http://127.0.0.1:8000/static/index.html
```

---


Connect to the database:
```bash
psql -U logistics_user -d logistics_tracking
```

Show the tables:
```sql
-- List all shipments
SELECT * FROM shipments;

-- List all shipment events
SELECT * FROM shipment_events;
```

---


## Contributions 🤝

Feel free to contribute, open issues, or suggest improvements!**
