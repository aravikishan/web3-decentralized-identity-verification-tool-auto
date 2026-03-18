from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3

# Initialize FastAPI app
app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
DATABASE = "identity_verification.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS UserIdentity (
                        user_id TEXT PRIMARY KEY,
                        documents TEXT,
                        verified BOOLEAN,
                        verification_date TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS VerificationHistory (
                        user_id TEXT,
                        document_id TEXT,
                        status TEXT,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Data models
class UserIdentity(BaseModel):
    user_id: str
    documents: List[str]
    verified: bool
    verification_date: datetime

class VerificationHistory(BaseModel):
    user_id: str
    document_id: str
    status: str
    timestamp: datetime

# Seed data
seed_data = [
    UserIdentity(user_id="user1", documents=["doc1", "doc2"], verified=True, verification_date=datetime.now()),
    UserIdentity(user_id="user2", documents=["doc3"], verified=False, verification_date=datetime.now())
]

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/verify", response_class=HTMLResponse)
async def verify_identity(request: Request):
    return templates.TemplateResponse("verify.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def user_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api-docs", response_class=HTMLResponse)
async def api_docs(request: Request):
    return templates.TemplateResponse("api_docs.html", {"request": request})

@app.post("/api/verify")
async def api_verify(user_identity: UserIdentity):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO UserIdentity (user_id, documents, verified, verification_date) VALUES (?, ?, ?, ?)",
                   (user_identity.user_id, ','.join(user_identity.documents), user_identity.verified, user_identity.verification_date))
    conn.commit()
    conn.close()
    return {"status": "Verification submitted"}

@app.get("/api/status/{user_id}")
async def api_status(user_id: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UserIdentity WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"user_id": row[0], "documents": row[1].split(','), "verified": row[2], "verification_date": row[3]}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/api/history/{user_id}")
async def api_history(user_id: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VerificationHistory WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    history = [{"user_id": row[0], "document_id": row[1], "status": row[2], "timestamp": row[3]} for row in rows]
    return {"history": history}
