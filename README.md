# Fully Functional Chatbot Backend

A FastAPI backend for an AI chatbot. Users sign in with Clerk, chat with a Mistral LLM (through LangChain), and get streamed replies. Every conversation is stored per user, and long conversations are kept short for the model with an automatic rolling summary.

![System diagram](docs/system-diagram.png)

## Features

- **Streaming chat** over Server-Sent Events (SSE).
- **Per-user chat sessions** with auto-generated titles.
- **Conversation memory**: the prompt combines a rolling session summary with the most recent messages.
- **Clerk authentication**: every chat endpoint verifies a Bearer JWT (RS256) and uses the `sub` claim as the user id.
- **Hot cache in Redis** (30 minute TTL) in front of the durable PostgreSQL store.
- **Alembic migrations** for the database schema.
- **Docker-ready** (Python 3.13 + `uv`).

## Tech stack

| Area | Technology |
| --- | --- |
| API | FastAPI, Uvicorn |
| LLM | LangChain + `langchain-mistralai` (Mistral) |
| Database | PostgreSQL, SQLAlchemy 2 (sync + asyncpg), Alembic |
| Cache | Redis |
| Auth | Clerk JWT, verified with PyJWT |
| Tooling | Python 3.13, `uv` |

## Project structure

```
main.py                     FastAPI app, registers the routers
src/
  config.py                 Environment-driven settings
  repository.py             Creates and holds the shared DB, Redis and LLM clients
  routes/                   HTTP routes (chat, chat_session, health)
  handlers/                 Request handling (streaming, structured, history, sessions)
  controller/               Business logic (sessions, saving turns)
    ai_controllers/         title_generator, session_summarizer
  prompts/                  Prompt templates (reply, title)
  db_actions/               PostgreSQL queries
  redis_actions/            Redis reads and writes
  models/                   SQLAlchemy models (ChatSession, Conversation)
  libs/                     Postgres, Redis and Mistral client factories
  utils/get_user.py         Clerk JWT verification dependency
alembic/                    Database migrations
Dockerfile
```

## API

All routes except the health check require `Authorization: Bearer <Clerk JWT>`.

| Method | Path | Description |
| --- | --- | --- |
| GET | `/` | Health check |
| POST | `/api/v1/chat/stream` | Send a message and stream the reply (SSE) |
| POST | `/api/v1/chat/structure` | Send a message and get the whole reply as JSON |
| GET | `/api/v1/chat/{id}?limit=10&skip=0` | Paginated message history of a session |
| GET | `/api/v1/chat_session/me` | List the signed-in user's chat sessions |
| DELETE | `/api/v1/chat_session/{chat_session_id}` | Delete one of the user's sessions |

Interactive docs are served at `/docs` when the app is running.

### Chat request body

```json
{
  "chat_session_id": null,
  "user_message": "Hello!"
}
```

Leave `chat_session_id` as `null` to start a new session.

### Stream format

```
event: session_id
data: <new session id>            (only when a session was just created)

data: {"content": "Hel"}
data: {"content": "lo!"}

data: [Done]
```

## How a message is processed

1. The request arrives with a Bearer JWT. It is verified with the Clerk public key and the user id is read from `sub`. An empty message returns `400`.
2. If there is no `chat_session_id`, a `chat_session` row is created and Mistral generates a title. The new id is sent first as a `session_id` event.
3. The prompt is built from the stored session summary, the last 6 messages and the new user message.
4. Mistral's reply is streamed back token by token as `data` events, followed by `[Done]`.
5. A background task saves the user and assistant messages to PostgreSQL and pushes them to Redis (last 4 messages kept).
6. Once the session has 4 or more stored messages, a summarizer asks Mistral to merge the old summary with the recent messages. The result is saved to Redis and PostgreSQL.

## Data model

- `chat_session`: `id`, `user_id`, `session_title` (max 60 chars), `session_summary`
- `conversation`: `id`, `session_id` (FK to `chat_session`, `ON DELETE CASCADE`), `role`, `content`, `additional_information` (JSON)

Redis keys (TTL 1800 seconds):

- `session:{id}:messages`: list holding the last 4 messages
- `session:{id}:summery`: the latest summary

## Getting started

### Prerequisites

- Python 3.13 and [`uv`](https://docs.astral.sh/uv/)
- A PostgreSQL database
- A Redis instance
- A Mistral API key
- A Clerk application (for the JWT public key)

### Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot

MISTRAL_API_KEY=your-mistral-api-key
MISTRAL_DEFAULT_MODEL=mistral-small-latest

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USER_NAME=
REDIS_PASSWORD=
REDIS_DATABASE_INDEX=0
REDIS_URL=

# PEM public key from Clerk; keep it on one line and write line breaks as \n
CLERK_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
```

`DATABASE_URL` must start with `postgresql://`; the async engine rewrites it to `postgresql+asyncpg://`. `mistral-small-latest` is only an example, so use any Mistral model you have access to.

### Run locally

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

The API is then available at <http://localhost:8000>.

### Run with Docker

```bash
docker build -t chatbot-backend .
docker run --env-file .env -p 8000:8000 chatbot-backend
```

The container listens on `$PORT` (default `8000`). It does not run migrations, so apply them to your database separately with `alembic upgrade head`.

### Database migrations

```bash
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```

## Known issues

- `POST /api/v1/chat/structure` is incomplete: `chat_response_generator_prompt` is async and needs a session id, but the handler calls it without `await` and without one, and `chat_session` is undefined when a session id is supplied. Use `/stream` for now.
- `session_summarizer.py` labels a message "User" only when its role is `user`, but messages are stored with the role `human`, so user messages are labelled "AI" in the summary prompt.
- SQLAlchemy engines are created with `echo=True`, which logs every SQL statement.
