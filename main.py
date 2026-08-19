import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile, Security, Form, Body
from fastapi.security import APIKeyHeader
from pywa import WhatsApp, types
import subprocess

load_dotenv()

PHONE_ID = os.getenv("WA_PHONE_ID")
TOKEN = os.getenv("WA_TOKEN")

PAPERLESS_WEBHOOK_TOKEN = os.getenv("PAPERLESS_WEBHOOK_TOKEN")
PAPERLESS_NOTIFICATION_NUMBERS = os.getenv("PAPERLESS_NOTIFICATION_NUMBERS").split(",")

app = FastAPI()  # FastAPI server

# Create a WhatsApp client
wa = WhatsApp(
    phone_id=PHONE_ID,
    token=TOKEN,
)

@app.get("/test")
def test():
    wa.send_message(
        to=PAPERLESS_NOTIFICATION_NUMBERS[0],
        text="Hello, world!"
    )
    return {"status": "ok"}

@app.post("/soil_moisture")
def soil_moisture(
    json: dict = Body(...),
):
    print(json)

    wa.send_message(
        to=PAPERLESS_NOTIFICATION_NUMBERS[0],
        text=f"Data: {json}"
    )

    return {"status": "ok"}

@app.post("/paperless-backup-notify")
def paperless_backup_notification(json: dict = Body(...)):

    percentage_full = json["percentage_full"]
    megabytes_free = json["megabytes_free"]


    for number in PAPERLESS_NOTIFICATION_NUMBERS:
        msg = wa.send_template(
            to=number,
            name="paperless_dvd_backup_alert_1",
            language=types.templates.TemplateLanguage.ENGLISH,
            params=[
                types.templates.BodyText.params(percentage_full, megabytes_free)
            ],
        )
        print(f"Sent notification to {number}: {msg}")
    return {"status": "ok"}

@app.get("/eject-tray")
def eject_tray():
    try:
        print("Opening DVD tray...")
        subprocess.run(["eject", "/dev/sr0"], check=True)
        return {"status": "ok"}
    except subprocess.CalledProcessError as e:
        print(f"Hardware error: {e}")
        return {"status": "error"}

@app.post("/paperless-document-notify")
def paperless_document_notification(
    api_key=Security(APIKeyHeader(name="X-API-Key")),
    file: UploadFile = File(...),
    title: str = Form(...),
    filename: str = Form(...),
):
    """Receive a POST webhook with X-API-Key header and a document in the form body."""
    if not PAPERLESS_WEBHOOK_TOKEN or not api_key:
        raise HTTPException(status_code=401, detail="Missing authorization")
    if api_key != PAPERLESS_WEBHOOK_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Document from form body (multipart/form-data)

    file_content = file.file.read()

    for number in PAPERLESS_NOTIFICATION_NUMBERS:
        msg = wa.send_template(
            to=number,
            name="voucher_reminder_1",
            language=types.templates.TemplateLanguage.ENGLISH_US,
            params=[
                types.templates.BodyText.params(
                    voucher_name=title,
                    expiry_date="less than 15 days",
                ),
                types.templates.HeaderDocument.params(
                    document=file_content,
                    filename=filename,
                    mime_type=file.content_type,
                ),
            ],
        )
        print(f"Sent notification to {number}: {msg}")
    return {"status": "ok"}
