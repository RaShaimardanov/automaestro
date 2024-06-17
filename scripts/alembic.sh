alembic init --template async alembic
alembic revision --autogenerate -m "First migration"
alembic upgrade head