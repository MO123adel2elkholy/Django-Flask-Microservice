# Django - Flask Microservice (RabbitMQ)

Small monorepo demonstrating two microservices communicating via RabbitMQ:

- admin (Django) — product management, publishes product events to queue `main`, consumes `admin` to process likes.
- main (Flask) — product read service, stores local product records, publishes like events to queue `admin`, consumes `main` to sync product create/update/delete.

## Repo layout
- /admin — Django project (manage.py, settings, products app, producer/consumer)
- /main — Flask microservice (main.py, consumer/producer, DB and migrations)
- .env — environment variables (not included; create locally)

## Prerequisites (Windows)
- Python 3.8+
- pip
- RabbitMQ (or CloudAMQP)
- Optional: Docker (to run RabbitMQ locally)

## Setup (Windows commands)
1. Create virtual env and install deps:
```powershell
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Create `.env` in repository root (example):
```env
CLOUDAMQP_URL=amqps://<user>:<pass>@<host>/<vhost>
SECRET_KEY=a-strong-secret-for-django
DATABASE_URL=sqlite:///products.db    # optional for Flask
```

3. Start RabbitMQ (optional via Docker):
```powershell
docker run -d --hostname rabbit --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## Running the services
Order recommendation: start RabbitMQ → Django (admin) → Django consumer → Flask (main) → Flask consumer.

Django (admin)
```powershell
cd admin
py manage.py migrate
py manage.py createsuperuser   # optional
py manage.py runserver 0.0.0.0:8000
# in another terminal (from admin folder) start the consumer that processes 'admin' queue:
py consumer.py
# optional: send test product events:
py products\producer.py
```

Flask (main)
```powershell
cd main
# If manager.py is present for migrations:
py manager.py db init
py manager.py db migrate
py manager.py db upgrade

# run API:
py main.py
# in another terminal (from main folder) start the consumer that processes 'main' queue:
py consumer.py
# optional: send test like events:
py producer.py
```

## API (Flask main)
- GET /api/products — returns products stored by Flask
- POST /api/products/<id>/like — likes a product (calls Django user endpoint, then publishes like event to `admin` queue)

Example:
```powershell
curl http://127.0.0.1:5000/api/products
curl -X POST http://127.0.0.1:5000/api/products/1/like
```

## Event flow summary
- Product created/updated/deleted in admin → admin producer publishes to queue `main` → Flask consumer updates local DB.
- Like event from frontend → Flask records user-product relation and publishes `product_liked` to queue `admin` → Django consumer increments product.likes.

Queue names used in code:
- product events → `main`
- like events → `admin`

## Environment variables
- CLOUDAMQP_URL — RabbitMQ URL (amqp or amqps)
- SECRET_KEY — Django secret key
- DATABASE_URL — optional DB URL for Flask (defaults to sqlite file `products.db`)

## Troubleshooting
- Ensure RabbitMQ is reachable and CLOUDAMQP_URL is correct.
- Check RabbitMQ management UI at http://localhost:15672 (if using Docker/local).
- Confirm consumers are running and using the same queue names (`main`, `admin`).
- If Flask like endpoint fails, ensure Django (user endpoint) is running at http://127.0.0.1:8000/api/user.

## Notes
- The repository uses SQLite by default for simplicity.
- This is an example/demo; do not use DEBUG=True or SECRET_KEY from `.env` in production.
