from fastapi import FastAPI
import requests
import os

app = FastAPI()

CLICKTRANS_BASE = os.getenv(
    "CLICKTRANS_BASE"
)

CLICKTRANS_EMAIL = os.getenv(
    "CLICKTRANS_EMAIL"
)

CLICKTRANS_PASSWORD = os.getenv(
    "CLICKTRANS_PASSWORD"
)

CLICKTRANS_HEADER_NAME = os.getenv(
    "CLICKTRANS_HEADER_NAME"
)

CLICKTRANS_HEADER_VALUE = os.getenv(
    "CLICKTRANS_HEADER_VALUE"
)


@app.get("/")
async def root():

    return {
        "status": "working"
    }


@app.get("/test-login")
async def test_login():

    url = (
        f"{CLICKTRANS_BASE}"
        "/api/login_check"
    )

    headers = {

        CLICKTRANS_HEADER_NAME:
        CLICKTRANS_HEADER_VALUE,

        "Content-Type":
        "application/json"

    }

    payload = {

        "username":
        CLICKTRANS_EMAIL,

        "password":
        CLICKTRANS_PASSWORD,

        "deviceUID":
        "PAKO-BOT"

    }

    r = requests.post(

        url,

        json=payload,

        headers=headers

    )

    return {

        "status":
        r.status_code,

        "response":
        r.text

    }