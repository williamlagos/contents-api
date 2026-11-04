# Contents API

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Django 5.x](https://img.shields.io/badge/django-5.x-green.svg)](https://www.djangoproject.com/)
[![Django Ninja](https://img.shields.io/badge/api-django--ninja-purple.svg)](https://django-ninja.rest-framework.com/)

**Contents API** is the headless content management system, federated social layer, Plethora digital publishing engine, and multi-rail e-commerce backend for the Contents platform.

---

## Architecture & Companion Packages

The backend integrates and orchestrates 5 companion packages:

1. **`django-plethora`**: Content engine for digital publications, `Spreadable` articles, and interactive `Playable` components.
2. **`django-dashboarder`**: Modernized administration dashboard with responsive widget styling.
3. **`django-ship`**: Multi-rail payments (Stripe Checkout, PayPal v2, Web3 EVM) and order fulfillment.
4. **`django-socialize`**: ActivityPub federation, actor identity, and decentralized note dispatch.
5. **`django-feedly`**: AI discovery feeds (trending, chronological) and semantic vector search.

---

## API Endpoints (OpenAPI v1)

Interactive Swagger/OpenAPI documentation is available at `/api/docs`.

| Prefix | Description | Key Endpoints |
|---|---|---|
| `/` | System Health | `GET /` |
| `/api/health` | Diagnostic Health | `GET /api/health` |
| `/api/contents/` | Headless CMS CRUD | `GET /`, `POST /`, `GET /count`, `GET /{id}`, `PATCH /{id}`, `DELETE /{id}` |
| `/api/cms/` | Plethora Publishing | `GET /spreadables`, `POST /spreadables`, `GET /playables`, `POST /playables` |
| `/api/social/` | ActivityPub Social | `GET /actors`, `GET /actors/{username}`, `POST /activities` |
| `/api/shop/` | Commerce & Payments | `GET /products`, `POST /checkout` |
| `/api/feeds/` | AI Discovery Feeds | `GET /trending`, `GET /chronological`, `POST /search` |

---

## Development Setup

```bash
# 1. Install dependencies with uv
uv pip install -e .

# 2. Run database migrations
python manage.py migrate

# 3. Start development server
python manage.py runserver
```

### Running Tests

```bash
# Using pytest
pytest

# Using Django test runner
python manage.py test contents.tests
```

### Docker Compose

```bash
docker compose up --build
```
