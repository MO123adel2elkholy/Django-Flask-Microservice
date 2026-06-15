# Django - Flask Microservice (RabbitMQ) + React Frontend

Monorepo demo: two Python microservices (Django "admin" and Flask "main") communicating via RabbitMQ, with a React frontend client.

- admin (Django) — product management, publishes product events to queue `main`, consumes `admin` to process likes.
- main (Flask) — product read service, stores local product records, publishes like events to queue `admin`, consumes `main` to sync product create/update/delete.
- react-crud-main (React + TypeScript) — frontend for public product listing and admin CRUD.

Repo layout
- /admin — Django project and admin-facing API
- /main — Flask microservice (products API, consumer/producer)
- /react-crud-main — React frontend (routes: `/`, `/admin/products`, `/admin/products/create`, `/admin/products/:id/edit`)
- .env — environment variables (create locally)

Frontend features
- Public product listing (main page)
- Admin UI to list, create and edit products
- Calls backend APIs to fetch products and trigger "like" actions
- Dev server runs on http://localhost:3000

Prerequisites (Windows)
- Python 3.8+
- Node.js & npm
- pip
- RabbitMQ (local or CloudAMQP)
- Optional: Docker (for RabbitMQ)

Environment (.env, repo root)
- CLOUDAMQP_URL — RabbitMQ URL (amqp/amqps)
- SECRET_KEY — Django secret
- DATABASE_URL — optional for Flask (defaults to sqlite file)

Backend setup (Windows)
1. Create & activate Python venv, install requirements:
```powershell
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
2. Create `.env` with the variables above.

Run RabbitMQ (optional Docker)
```powershell
docker run -d --hostname rabbit --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Run Django (admin)
```powershell
cd admin
py manage.py migrate
py manage.py createsuperuser   # optional
py manage.py runserver 0.0.0.0:8000
# in another terminal (admin folder) start the Django consumer:
py consumer.py
# optional: publish product events for testing:
py products\producer.py
```

Run Flask (main)
```powershell
cd main
# run DB migrations if manager.py exists:
py manager.py db init
py manager.py db migrate
py manager.py db upgrade

# start API:
py main.py

# in another terminal (main folder) start the Flask consumer:
py consumer.py
# optional: publish like events for testing:
py producer.py
```

Frontend (React) setup & run
```powershell
cd react-crud-main
npm install
npm start
```
- Dev server: http://localhost:3000
- If the frontend needs different backend URLs, update API base URLs in the React source (or add REACT_APP_API_URL env var and use it in the code).

Build frontend for production
```powershell
cd react-crud-main
npm run build
# serve the build directory with your static server of choice
```

API endpoints used by frontend
- GET /api/products — list products (Flask main)
- POST /api/products/<id>/like — like a product (Flask main → publishes like to Django)

Event flow
- Product created/updated/deleted in admin → admin producer publishes to queue `main` → Flask consumer syncs local DB.
- Like from frontend → Flask records user-product and publishes `product_liked` to queue `admin` → Django consumer increments product.likes.

Troubleshooting
- Ensure CLOUDAMQP_URL is reachable and both services use the same queue names (`main`, `admin`).
- Check RabbitMQ management UI (if running locally) at http://localhost:15672.
- Ensure CORS is enabled (both services include CORS middlewares/config).

Notes
- Default DB: SQLite for local development.
- This project is a demo — do not use DEBUG=True or weak SECRET_KEY in production.
