from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()
notifications: List[dict] = []

class Notification(BaseModel):
    subject: str
    message: str

@app.post("/api/notify")
async def receive_notification(notification: Notification):
    notifications.append({
        "subject": notification.subject,
        "message": notification.message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return {"status": "Notification received"}

@app.get("/", response_class=HTMLResponse)
async def get_notifications():
    html_content = "<h1>📩 Notifications</h1>"
    if not notifications:
        html_content += "<p>No notifications received yet.</p>"
    else:
        for note in reversed(notifications):
            html_content += f"""
            <div style='padding:10px; border:1px solid #ccc; margin-bottom:10px;'>
                <strong>{note['subject']}</strong><br/>
                <small>{note['timestamp']}</small><br/>
                <p>{note['message']}</p>
            </div>
            """
    return html_content

