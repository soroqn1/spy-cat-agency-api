# Spy Cat Agency API

REST API for managing spy cats and their missions

## Quick Start

```bash
# Run
docker-compose up --build

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

API: http://localhost:8000  
Admin: http://localhost:8000/admin

## Endpoints

**Cats**
- `GET /api/cats/` - list all
- `POST /api/cats/` - create
- `PATCH /api/cats/{id}/` - update salary only
- `DELETE /api/cats/{id}/` - delete

**Missions**
- `GET /api/missions/` - list all
- `POST /api/missions/` - create (1-3 targets required)
- `POST /api/missions/{id}/assign_cat/` - assign cat
- `DELETE /api/missions/{id}/` - delete (only if cat=null)

**Targets**
- `PATCH /api/missions/{id}/targets/{target_id}/` - update notes/complete

## Postman

Import `postman_collection.json` into Postman.

## Stack

Django • DRF • PostgreSQL • Docker