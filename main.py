from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        # Insert meeting into Supabase
        url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
        headers = {
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        data = meeting.model_dump()  # Updated for Pydantic v2
        # Accept both string and list for with_whom
        if isinstance(data["with_whom"], str):
            # Split comma-separated names
            data["with_whom"] = [name.strip() for name in data["with_whom"].split(",")]
        
        # Convert datetime-local format to ISO format for Supabase
        if data["when"]:
            # Ensure proper timestamp format
            when_value = data["when"]
            # If it doesn't have seconds, add them
            if when_value.count(":") == 1:
                when_value = when_value + ":00"
            # Add timezone if not present (assume UTC)
            if "Z" not in when_value and "+" not in when_value and "-" not in when_value[-6:]:
                when_value = when_value + "Z"
            data["when"] = when_value
        
        logger.info(f"Sending data to Supabase: {data}")
        resp = requests.post(url, headers=headers, json=data)
        logger.info(f"Supabase response: {resp.status_code} - {resp.text}")
        
        if resp.status_code in (200, 201, 204):
            return {"message": "Meeting saved", "data": resp.json() if resp.text else None}
        else:
            error_detail = resp.text if resp.text else "Unknown Supabase error"
            logger.error(f"Supabase error: {error_detail}")
            raise HTTPException(status_code=500, detail=f"Supabase error: {error_detail}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving meeting: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

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