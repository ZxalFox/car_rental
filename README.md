# Car Rental – Django + DRF + Postgres (Docker)

## Subir em 3 passos
1. `docker compose up --build`
2. Acesse Admin: http://localhost:8000/admin/ (admin / admin123)
3. API: http://localhost:8000/api/  (endpoints: /cars/, /customers/, /rentals/)

## Comandos úteis
- `docker compose exec web python manage.py createsuperuser`
- `docker compose exec web python manage.py shell`
- `docker compose logs -f web`
