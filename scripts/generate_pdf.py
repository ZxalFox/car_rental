from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple

from fpdf import FPDF

# (text, style) entries used to populate the PDF. Styles: title, subtitle, h1, h2, p.
CONTENT: Tuple[Tuple[str, str], ...] = (
    ("Car Rental - Visao Tecnica", "title"),
    (f"Data: {datetime.now():%d/%m/%Y}", "subtitle"),
    ("1. Visao Geral do Repositorio", "h1"),
    (
        "- Projeto full stack de locacao de veiculos com Django 5, Django REST Framework e PostgreSQL.\n"
        "- Orquestracao via Docker Compose com servicos para backend, banco e frontend Gatsby.\n"
        "- Estrutura pronta para autenticacao baseada no modelo personalizado Customer (extends AbstractUser).",
        "p",
    ),
    ("2. Backend Django", "h1"),
    ("Arquitetura", "h2"),
    (
        "- App principal `rental` concentra models, forms, views e API.\n"
        "- Configuracoes em `config/settings.py`, com suporte a variaveis .env, Postgres e fallback SQLite.",
        "p",
    ),
    ("Modelagem", "h2"),
    (
        "- Car: identifica veiculos com placa unica, diaria configuravel e flag de disponibilidade.\n"
        "- Customer: usuario autenticavel com campos extras (documento, telefone, etc.).\n"
        "- Rental: reserva vinculando carro e cliente, controla status (reservada, em curso, finalizada, cancelada) e calcula preco total evitando sobreposicao de datas.",
        "p",
    ),
    ("API REST", "h2"),
    (
        "- DRF com paginacao padrao e autenticacao de sessao (SessionAuthentication).\n"
        "- Viewsets: CarViewSet, CustomerViewSet (apenas staff), RentalViewSet com escopo por usuario e acoes auxiliares (my).\n"
        "- Serializers expoem detalhes aninhados (car_detail) e protegem campos calculados.\n"
        "- Endpoints adicionais de sessao: /api/session/, /api/session/login/, /api/session/logout/.",
        "p",
    ),
    ("Infraestrutura", "h2"),
    (
        "- compose/local/Dockerfile monta o servico web com Python 3.12, aplica migracoes e cria superusuario.\n"
        "- docker-compose.yml define servicos web, db e gatsby, compartilha volumes e expoe portas 8000/8001.\n"
        "- CORS configurado (django-cors-headers) para permitir consumo pelo Gatsby.\n"
        "- Script de entrada garante migrations automaticas e criacao de usuario admin para testes.",
        "p",
    ),
    ("3. Frontend Django (Templates)", "h1"),
    (
        "- Renderiza HTML server-side com Pico.css via templates/.\n"
        "- Painel (/) mostra reservas do usuario e carros ativos com formularios baseados em RentalForm.\n"
        "- Fluxo de reserva em /rentals/nova/ usa CSRF padrao, validacoes server-side e redireciona via CBVs.\n"
        "- Autenticacao aproveita as views nativas de django.contrib.auth.",
        "p",
    ),
    ("4. Frontend Gatsby (SPA)", "h1"),
    ("Arquitetura", "h2"),
    (
        "- Projeto React/Gatsby em frontend/ com build Node 20 e hot reload (porta 8001).\n"
        "- Contexto global de autenticacao (AuthContext) conversa com os endpoints de sessao (cookies).\n"
        "- Cliente generico api/client.js centraliza fetch com CSRF e credenciais.\n"
        "- Paginas principais: dashboard (index.js), login (login.js), criacao de reserva (rentals/nova.js).",
        "p",
    ),
    ("UX e Dados", "h2"),
    (
        "- Dashboard consome /api/cars/ e /api/rentals/my/, exibe resumo, tabela de reservas e cartoes de carros.\n"
        "- Formulario SPA replica campos do Django, preenche diaria automaticamente e trata erros da API em linha.\n"
        "- Navegacao client-side com Link, feedback visual via alerts e componentes reutilizaveis.\n"
        "- Build preparado para producao (npm run build) e integrado ao Docker Compose.\n",
        "p",
    ),
    ("5. Comparativo Gatsby x Django Templates", "h1"),
    ("Renderizacao", "h2"),
    (
        "- Django entrega HTML gerado no servidor; Gatsby gera SPA estatica com hidratacao React.\n"
        "- Gatsby permite navegacao instantanea e mudancas de estado sem reload; Django depende de round-trips.\n",
        "p",
    ),
    ("Consumo de Dados", "h2"),
    (
        "- Django usa ORM diretamente nas views, contexto passado ao template.\n"
        "- Gatsby atua como cliente da API REST, respeitando regras de autenticacao via cookies.\n",
        "p",
    ),
    ("Autenticacao", "h2"),
    (
        "- Templates usam sessao tradicional com formularios Django e protecao CSRF automatica.\n"
        "- Gatsby reutiliza a mesma sessao com chamadas /api/session/*, mantendo cookies e estado no contexto.\n",
        "p",
    ),
    ("Formularios", "h2"),
    (
        "- Django depende de RentalForm para validacao server-side e rendering automatico.\n"
        "- Gatsby implementa formulario controlado em React, exibindo mensagens de erro retornadas pela API.\n",
        "p",
    ),
    ("Build e Deploy", "h2"),
    (
        "- Django roda via Gunicorn/Daphne dentro do container web, servindo templates.\n"
        "- Gatsby constroi assets estaticos (ou roda gatsby develop) em container Node separado, consumindo a API.\n",
        "p",
    ),
    ("6. Proximos Passos Sugeridos", "h1"),
    (
        "- Automatizar limpeza de cache do Gatsby para evitar problemas de permissao em builds locais.\n"
        "- Adicionar testes end-to-end cobrindo o fluxo SPA (Playwright ou Cypress).\n"
        "- Avaliar GraphQL do Gatsby ou bibliotecas de cache cliente (SWR/React Query).\n"
        "- Implementar internacionalizacao compartilhada entre os dois frontends.",
        "p",
    ),
)

REPLACEMENTS = {
    "–": "-",
    "—": "-",
    "•": "-",
    "ç": "c",
    "Ç": "C",
    "ã": "a",
    "Ã": "A",
    "õ": "o",
    "Õ": "O",
    "á": "a",
    "Á": "A",
    "é": "e",
    "É": "E",
    "í": "i",
    "Í": "I",
    "ó": "o",
    "Ó": "O",
    "ú": "u",
    "Ú": "U",
    "â": "a",
    "Â": "A",
    "ê": "e",
    "Ê": "E",
    "ô": "o",
    "Ô": "O",
    "à": "a",
    "À": "A",
    "º": "o",
    "ª": "a",
}


def as_ascii(text: str) -> str:
    """Replace non-ASCII characters with ASCII-friendly fallbacks."""
    result = []
    for char in text:
        if ord(char) < 128:
            result.append(char)
        else:
            result.append(REPLACEMENTS.get(char, "?"))
    return "".join(result)


class TechnicalPDF(FPDF):
    """Small helper around FPDF tuned for our layout."""

    def __init__(self) -> None:
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_author("Car Rental Project")
        self.set_title(as_ascii("Car Rental - Visao Tecnica"))

    @property
    def effective_width(self) -> float:
        """Width available for content after subtracting margins."""
        return self.w - self.l_margin - self.r_margin

    def write_content(self, entries: Iterable[Tuple[str, str]]) -> None:
        for raw_text, style in entries:
            text = as_ascii(raw_text)
            self.set_x(self.l_margin)

            if style == "title":
                self.set_font("Helvetica", "B", 18)
                self.multi_cell(self.effective_width, 10, text)
                self.ln(2)
            elif style == "subtitle":
                self.set_font("Helvetica", "", 12)
                self.multi_cell(self.effective_width, 8, text)
                self.ln(4)
            elif style == "h1":
                self.set_font("Helvetica", "B", 14)
                self.multi_cell(self.effective_width, 8, text)
                self.ln(2)
            elif style == "h2":
                self.set_font("Helvetica", "B", 12)
                self.multi_cell(self.effective_width, 7, text)
            else:
                self.set_font("Helvetica", "", 11)
                self.multi_cell(self.effective_width, 6, text)
                self.ln(1)


def build_pdf(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = TechnicalPDF()
    pdf.write_content(CONTENT)
    pdf.output(str(output_path))


if __name__ == "__main__":
    build_pdf(Path("docs/carrental_visao_tecnica.pdf"))
