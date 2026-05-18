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

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "CHAT_ID"
)


def send_telegram(text):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    requests.post(

        url,

        json={

            "chat_id":
            CHAT_ID,

            "text":
            text

        }

    )


def get_token():

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

        headers=headers,

        json=payload

    )

    return r.json()["token"]


@app.get("/")
async def root():

    return {

        "status":
        "working"

    }


@app.get("/test-login")
async def test_login():

    token = get_token()

    return {

        "jwt":
        token[:100]

    }


@app.get("/test-auction/{auction_id}")
async def test_auction(
    auction_id: int
):

    token = get_token()

    headers = {

        CLICKTRANS_HEADER_NAME:
        CLICKTRANS_HEADER_VALUE,

        "Authorization":
        f"Bearer {token}"

    }

    url = (

        f"{CLICKTRANS_BASE}"

        f"/api/mobile/auction/{auction_id}"

    )

    r = requests.get(

        url,

        headers=headers

    )

    return r.json()


@app.post(
    "/webhook/new-auction"
)
async def new_auction(
    data: dict
):

    title = data.get(
        "title",
        "No title"
    )

    auction_id = data.get(
        "id",
        "?"
    )

    message = f"""

🚛 NEW CLICKTRANS

📦 {title}

ID: {auction_id}

🔍 https://web-production-05a5a.up.railway.app/test-auction/{auction_id}

"""

    send_telegram(
        message
    )

    return {

        "ok":
        True

    }