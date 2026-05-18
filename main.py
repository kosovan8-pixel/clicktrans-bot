from fastapi import FastAPI
import requests
from requests.auth import HTTPBasicAuth
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

    headers = {
        CLICKTRANS_HEADER_NAME:
        CLICKTRANS_HEADER_VALUE
    }

    auth = HTTPBasicAuth(
        CLICKTRANS_EMAIL,
        CLICKTRANS_PASSWORD
    )

    urls = [

        "/api/login_check",

        "/api/login",

        "/api/auth/login",

        "/swagger",

        "/api"

    ]

    result = {}

    for url in urls:

        r = requests.get(

            f"{CLICKTRANS_BASE}{url}",

            headers=headers,

            auth=auth

        )

        result[url] = {

            "status":
            r.status_code,

            "response":
            r.text[:300]

        }

    return result