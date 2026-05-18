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

    headers = {
        CLICKTRANS_HEADER_NAME:
        CLICKTRANS_HEADER_VALUE,

        "Content-Type":
        "application/json"
    }

    variants = [

        {
            "username":
            CLICKTRANS_EMAIL,

            "password":
            CLICKTRANS_PASSWORD
        },

        {
            "email":
            CLICKTRANS_EMAIL,

            "password":
            CLICKTRANS_PASSWORD
        },

        {
            "_username":
            CLICKTRANS_EMAIL,

            "_password":
            CLICKTRANS_PASSWORD
        },

        {
            "username":
            CLICKTRANS_EMAIL,

            "password":
            CLICKTRANS_PASSWORD,

            "deviceUID":
            "PAKO-BOT"
        }

    ]

    result = {}

    for i, payload in enumerate(
        variants,
        start=1
    ):

        r = requests.post(

            f"{CLICKTRANS_BASE}/api/login_check",

            json=payload,

            headers=headers

        )

        result[
            f"v{i}"
        ] = {

            "variant":
            i,

            "status":
            r.status_code,

            "response":
            r.text

        }

    return result