# BE-02 — CRUD API with SQLite

FastAPI CRUD task API migrated from in-memory storage to SQLite.

## Architecture
`Client -> FastAPI -> SQLite (tasks.db)`

The five CRUD endpoints stay the same; only the storage layer changes.

## Run
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## Database
SQLite was chosen because it is lightweight, requires no separate database server, and stores data in one file. `tasks.db` is created automatically. The `tasks` table is also created automatically, and three seed tasks are inserted only when the table is empty.

`tasks.db` is git-ignored so a clone creates its own local database.

## Endpoints
- GET `/tasks`
- GET `/tasks/{id}`
- POST `/tasks`
- PUT `/tasks/{id}`
- DELETE `/tasks/{id}`

## Status codes
200 read/update, 201 create, 204 delete, 400 invalid body, 404 unknown id.

## SQL used
```sql
SELECT * FROM tasks;
SELECT * FROM tasks WHERE done = 1;
SELECT COUNT(*) FROM tasks;
UPDATE tasks SET done = 1;
DELETE FROM tasks WHERE done = 1;
```

## Parameterized queries
Values are passed through `?` placeholders rather than concatenated into SQL, e.g.:
```python
c.execute("SELECT id,title,done FROM tasks WHERE id=?",(task_id,))
```

## Stage 4 evidence
Add the real DB Browser for SQLite screenshot at `docs/database-screenshot.png`.

## Stage 6 — optional AI rematch
See `prompts/ai-rematch-prompt.txt`. Keep any AI-generated comparison in a separate folder/branch and add an `AI vs me` section to this README if you complete the bonus.
