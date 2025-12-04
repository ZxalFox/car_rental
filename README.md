# Car Rental – Django + DRF + Postgres (Docker)

## Subir em 3 passos

1. `docker compose up --build`
2. Acesse Admin: http://localhost:8000/admin/ (admin / admin123)
3. Frontend Gatsby: http://localhost:8001/

> O Gatsby consome a API Django. Ajuste as variáveis `GATSBY_API_URL` e `GATSBY_RENTAL_URL` no `.env` caso queira apontar para outro host.

### Variáveis úteis

- `CORS_ALLOWED_ORIGINS`: lista de origens permitidas (separadas por vírgula) para chamadas ao Django.
- `CSRF_TRUSTED_ORIGINS`: origens confiáveis para envio de cookies ou sessões.
- `GATSBY_API_URL`: URL base usada pelo Gatsby para consumir a API.
- `GATSBY_RENTAL_URL`: URL usada para redirecionar para o fluxo de reserva existente no Django.

## Comandos úteis

- `docker compose exec web python manage.py createsuperuser`
- `docker compose exec web python manage.py shell`
- `docker compose logs -f web`
- `docker compose logs -f gatsby`

## Estrutura implementada

- **Frontend web (Django templates)**: o app `rental` expõe um painel simples (`/`) com listagem das reservas do usuário autenticado e carros disponíveis, além de um formulário para nova reserva (`/rentals/nova/`). As views ficam em `rental/views.py` e os templates em `templates/rental/`.
- **Frontend Gatsby (SPA)**: vive em `frontend/`, roda em http://localhost:8001/ e reutiliza a API `/rental/api/`. A página inicial lista carros disponíveis consumindo a API com CORS liberado.
- **Fluxo de autenticação unificado**: realize login em http://localhost:8001/login/ usando as mesmas credenciais do Django. As sessões são gerenciadas pela própria API (endpoints `/api/session/`).
- **Autenticação pronta para uso**: rotas padrão do Django em `/accounts/login` e `/accounts/logout`, com redirecionamento automático para o painel. O modelo `Customer` continua sendo a tabela de usuários e recebe os dados de autenticação.
- **Regra de negócio centralizada**: a classe `Rental` garante que um carro não possa ser reservado em períodos que se sobreponham (usada na API, formulário e model `clean()`). O valor total é calculado automaticamente com base na diária e na duração.
- **API REST isolada**: os endpoints continuam disponíveis em `/api/cars/`, `/api/customers/` e `/api/rentals/`, definidos em `rental/api_urls.py`.

## Documentação Adicional

- [Comparativo Técnico: Django Templates vs Gatsby](docs/comparison_django_gatsby.md): Uma análise detalhada das diferenças arquiteturais e de experiência entre as duas abordagens implementadas neste projeto.
