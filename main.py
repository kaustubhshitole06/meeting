from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

app = FastAPI()

# Supabase config
SUPABASE_URL = "https://alyjyarqzaoldlbczawz.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFseWp5YXJxemFvbGRsYmN6YXd6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwMzUxMjgsImV4cCI6MjA3MzYxMTEyOH0.MnXRA02qvHZQXKYqU3EtR3csOTKvF2HN2H3uuzM4Sio"
SUPABASE_TABLE = "meetings"

# Serve static files from current directory
app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import Union

class Meeting(BaseModel):
    with_whom: Union[str, list[str]]
    when: str

@app.post("/meetings")
def create_meeting(meeting: Meeting):
    # Insert meeting into Supabase
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = meeting.dict()
    # Accept both string and list for with_whom
    if isinstance(data["with_whom"], str):
        data["with_whom"] = [data["with_whom"]]
    resp = requests.post(url, headers=headers, json=[data])
    if resp.status_code in (200, 201):
        return {"message": "Meeting saved"}
    else:
        raise HTTPException(status_code=500, detail=f"Supabase error: {resp.text}")

@app.get("/meetings")
def get_meetings():
    # Fetch meetings from Supabase
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=*"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise HTTPException(status_code=500, detail=f"Supabase error: {resp.text}")

@app.get("/")
def read_root():
    html_path = os.path.join(os.path.dirname(__file__), "meeting.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="meeting.html not found")
    try:
        return FileResponse(html_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving meeting.html: {e}")