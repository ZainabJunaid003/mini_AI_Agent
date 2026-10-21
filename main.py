import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import load_docs
from agent import run_agent

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

db = sqlite3.connect("chat.db", check_same_thread=False)
db.execute("CREATE TABLE IF NOT EXISTS messages "
           "(id INTEGER PRIMARY KEY, role TEXT, content TEXT)")

@app.on_event("startup")
def startup():
    load_docs("docs")

class ChatIn(BaseModel):
    message: str

@app.post("/chat")
def chat(body: ChatIn):
    rows = db.execute("SELECT role, content FROM messages "
                      "ORDER BY id DESC LIMIT 10").fetchall()[::-1]
    history = [{"role": r, "content": c} for r, c in rows]
    answer, tin, tout = run_agent(history, body.message)
    db.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", body.message))
    db.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", answer))
    db.commit()
    return {"reply": answer, "tokens_in": tin, "tokens_out": tout}