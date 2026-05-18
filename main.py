from fastapi import FastAPI
import requests
import os

app = FastAPI()

# =========================
# TELEGRAM
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# CLICKTRANS
# =========================

CLICKTRANS_EMAIL = os.getenv(
    "CLICKTRANS_EMAIL"
)

CLICKTRANS_PASSWORD = os.getenv(
    "CLICKTRANS_PASSWORD"
)

HEADER_NAME = os.getenv(
    "CLICKTRANS_HEADER_NAME"
)

HEADER_VALUE = os.getenv(
    "CLICKTRANS_HEADER_VALUE"
)

BASE = os.getenv(
    "CLICKTRANS_BASE",
    "https://staging-02.develop.clicktrans.pl"
)


@app.get("/")
async def root():

    return {
        "status": "working"
    }


# =========================
# TELEGRAM
# =========================

def send_telegram_message(text):

    if not BOT_TOKEN:
        return

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": text
    }

    r = requests.post(
        url,
        json=data
    )

    print(r.text)


@app.get("/test-telegram")
async def test_telegram():

    send_telegram_message(
        "🔥 Railway Telegram OK"
    )

    return {
        "ok": True
    }


# =========================
# CLICKTRANS LOGIN
# =========================

def get_jwt():

    url = (
        f"{BASE}"
        f"/api/login_check"
    )

    payload = {
        "username":
            CLICKTRANS_EMAIL,

        "password":
            CLICKTRANS_PASSWORD
    }

    headers = {
        HEADER_NAME:
            HEADER_VALUE,

        "Content-Type":
            "application/x-www-form-urlencoded"
    }

    r = requests.post(
        url,
        data=payload,
        headers=headers
    )

    print(
        "STATUS:",
        r.status_code
    )

    print(
        "TEXT:",
        r.text
    )

    if r.status_code != 200:

        return {
            "error": True,
            "status":
                r.status_code,

            "response":
                r.text
        }

    try:

        return r.json()

    except Exception:

        return {
            "error":
                "invalid json",

            "response":
                r.text
        }


@app.get("/test-login")
async def test_login():

    token = get_jwt()

    return token


# =========================
# AUCTION TEST
# =========================

@app.get(
    "/test-auction/{auction_id}"
)
async def test_auction(
    auction_id: int
):

    jwt_data = get_jwt()

    print(jwt_data)

    token = (
        jwt_data.get(
            "token"
        )

        or

        jwt_data.get(
            "jwt"
        )

        or

        jwt_data.get(
            "access_token"
        )
    )

    if not token:

        return {
            "error":
                "JWT not found",

            "response":
                jwt_data
        }

    headers = {

        "Authorization":
            f"Bearer {token}",

        HEADER_NAME:
            HEADER_VALUE
    }

    url = (
        f"{BASE}"
        f"/api/mobile/"
        f"auction/"
        f"{auction_id}"
    )

    r = requests.get(
        url,
        headers=headers
    )

    return {
        "status":
            r.status_code,

        "response":
            r.text
    }


# =========================
# NEW AUCTION WEBHOOK
# =========================

@app.post(
    "/webhook/new-auction"
)
async def new_auction(
    data: dict
):

    print(
        "NEW AUCTION"
    )

    print(data)

    title = data.get(
        "title",
        "No title"
    )

    from_city = data.get(
        "fromLocalizationShort",
        "Unknown"
    )

    to_city = data.get(
        "toLocalizationShort",
        "Unknown"
    )

    budget = data.get(
        "budget",
        "-"
    )

    message = f"""
🚛 NEW AUCTION

📦 {title}

📍 {from_city}
➡️ {to_city}

💰 Budget: {budget}
"""

    send_telegram_message(
        message
    )

    return {
        "ok": True
    }


# =========================
# UPDATE WEBHOOK
# =========================

@app.post(
    "/webhook/update-auction"
)
async def update_auction(
    data: dict
):

    print(
        "UPDATED AUCTION"
    )

    print(data)

    return {
        "ok": True
    }