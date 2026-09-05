from contextlib import closing
from pathlib import Path
import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
DB_PATH = Path(__file__).resolve().parent / "tasks.db"
app = FastAPI(title="Task CRUD API", version="2.0")
class TaskIn(BaseModel):
    title: str
    done: bool = False
def conn():
    c=sqlite3.connect(DB_PATH)
    c.row_factory=sqlite3.Row
    return c
def init_db():
    with closing(conn()) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0)""")
        if c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
            c.executemany("INSERT INTO tasks(title,done) VALUES(?,?)",
                          [("Learn FastAPI",0),("Connect SQLite database",0),("Test CRUD endpoints",0)])
        c.commit()
@app.on_event("startup")
def startup(): init_db()
def out(r): return {"id":r["id"],"title":r["title"],"done":bool(r["done"])}
@app.get("/tasks")
def all_tasks():
    with closing(conn()) as c:
        rows=c.execute("SELECT id,title,done FROM tasks ORDER BY id").fetchall()
    return [out(r) for r in rows]
@app.get("/tasks/{task_id}")
def one_task(task_id:int):
    with closing(conn()) as c:
        r=c.execute("SELECT id,title,done FROM tasks WHERE id=?",(task_id,)).fetchone()
    if r is None: return JSONResponse(status_code=404, content={"error": "Task not found"})
    return out(r)
@app.post("/tasks",status_code=201)
def create(task:TaskIn):
    if not task.title.strip(): return JSONResponse(status_code=400, content={"error": "Title is required"})
    with closing(conn()) as c:
        cur=c.execute("INSERT INTO tasks(title,done) VALUES(?,?)",(task.title.strip(),int(task.done)))
        c.commit()
        r=c.execute("SELECT id,title,done FROM tasks WHERE id=?",(cur.lastrowid,)).fetchone()
    return out(r)
@app.put("/tasks/{task_id}")
def update(task_id:int,task:TaskIn):
    if not task.title.strip(): return JSONResponse(status_code=400, content={"error": "Title is required"})
    with closing(conn()) as c:
        if c.execute("SELECT id FROM tasks WHERE id=?",(task_id,)).fetchone() is None:
            return JSONResponse(status_code=404, content={"error": "Task not found"})
        c.execute("UPDATE tasks SET title=?,done=? WHERE id=?",(task.title.strip(),int(task.done),task_id))
        c.commit()
        r=c.execute("SELECT id,title,done FROM tasks WHERE id=?",(task_id,)).fetchone()
    return out(r)
@app.delete("/tasks/{task_id}",status_code=204)
def delete(task_id:int):
    with closing(conn()) as c:
        if c.execute("SELECT id FROM tasks WHERE id=?",(task_id,)).fetchone() is None:
            return JSONResponse(status_code=404, content={"error": "Task not found"})
        c.execute("DELETE FROM tasks WHERE id=?",(task_id,))
        c.commit()
    return None