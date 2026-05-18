from fastapi import FastAPI
import requests
import os

app = FastAPI()

CLICKTRANS_EMAIL = os.getenv("CLICKTRANS_EMAIL")
CLICKTRANS_PASSWORD = os.getenv("CLICKTRANS_PASSWORD")

HEADER_NAME = os.getenv("CLICKTRANS_HEADER_NAME")
HEADER_VALUE = os.getenv("CLICKTRANS_HEADER_VALUE")

BASE = os.getenv(
    "CLICKTRANS_BASE",
    "https://staging-02.develop.clicktrans.pl"
)


@app.get("/")
async def root():
    return {"status": "working"}


def get_jwt():

    url = f"{BASE}/api/login_check"

    payload = {
        "username": CLICKTRANS_EMAIL,
        "password": CLICKTRANS_PASSWORD,
        "deviceUID": "web-test"
    }

    headers = {
        HEADER_NAME: HEADER_VALUE
    }

    r = requests.post(
        url,
        json=payload,
        headers=headers
    )

    print(r.text)

    return r.json()


@app.get("/test-login")
async def test_login():

    token = get_jwt()

    return token


@app.get("/test-auction/{auction_id}")
async def test_auction(auction_id: int):

    jwt_data = get_jwt()

    token = jwt_data["token"]

    headers = {
        "Authorization": f"Bearer {token}",
        HEADER_NAME: HEADER_VALUE
    }

    url = f"{BASE}/api/mobile/auction/{auction_id}"

    r = requests.get(
        url,
        headers=headers
    )

    return r.json()


@app.post("/webhook/new-auction")
async def new_auction(data: dict):

    print(data)

    return {"ok": True}


@app.post("/webhook/update-auction")
async def update_auction(data: dict):

    print("UPDATED")

    print(data)

    return {"ok": True}