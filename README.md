# Car Rental – Django + DRF + Postgres (Docker)

## Subir em 3 passos

1. `docker compose up --build`
2. Acesse Admin: http://localhost:8000/admin/ (admin / admin123)
3. API: http://localhost:8000/api/ (endpoints: /cars/, /customers/, /rentals/)

## Comandos úteis

- `docker compose exec web python manage.py createsuperuser`
- `docker compose exec web python manage.py shell`
- `docker compose logs -f web`

## Estrutura implementada

- **Frontend web (Django templates)**: o app `rental` expõe um painel simples (`/`) com listagem das reservas do usuário autenticado e carros disponíveis, além de um formulário para nova reserva (`/rentals/nova/`). As views ficam em `rental/views.py` e os templates em `templates/rental/`.
- **Autenticação pronta para uso**: rotas padrão do Django em `/accounts/login` e `/accounts/logout`, com redirecionamento automático para o painel. O modelo `Customer` continua sendo a tabela de usuários e recebe os dados de autenticação.
- **Regra de negócio centralizada**: a classe `Rental` garante que um carro não possa ser reservado em períodos que se sobreponham (usada na API, formulário e model `clean()`). O valor total é calculado automaticamente com base na diária e na duração.
- **API REST isolada**: os endpoints continuam disponíveis em `/api/cars/`, `/api/customers/` e `/api/rentals/`, definidos em `rental/api_urls.py`.
