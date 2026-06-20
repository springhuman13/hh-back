# 🚀 HaHackathon Backend

Backend API for a web platform that helps hackathon participants find teammates, create teams and match candidates based on their skills.

The application provides authentication, profile management, team management, file storage and a recommendation algorithm for matching users with teams.

---

## Features

- User authentication
- Telegram Login
- JWT authorization
- User profiles
- Team management
- Skill-based team matching
- File upload to Amazon S3
- Hackathon management
- REST API

---

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- Pydantic
- JWT
- Amazon S3

---

## Architecture

```
routers/
services/
repositories/
models/
schemas/
database/
```

The project follows a layered architecture that separates API endpoints, business logic and database access.

---

## Getting Started

```bash
docker compose up --build
```

or

```bash
uvicorn app.main:app --reload
```

---

## Matching Algorithm

The recommendation system ranks teams using several parameters:

- user role
- available positions
- technical focus
- skill checklist
- weighted skill scores

---

## Roadmap

- [ ] Automated tests
- [ ] CI/CD
- [ ] Caching
- [ ] WebSockets
- [ ] OpenAPI improvements

---

## License

MIT
