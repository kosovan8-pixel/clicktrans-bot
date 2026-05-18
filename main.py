from fastapi import FastAPI
import requests
import os

app = FastAPI()

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


def test_request(
    name,
    payload,
    use_json=True
):

    url = (
        f"{BASE}"
        f"/api/login_check"
    )

    headers = {
        HEADER_NAME:
            HEADER_VALUE
    }

    if use_json:

        r = requests.post(
            url,
            json=payload,
            headers=headers
        )

    else:

        r = requests.post(
            url,
            data=payload,
            headers=headers
        )

    return {
        "name": name,
        "status": r.status_code,
        "response": r.text
    }


@app.get("/test-login")
async def test_login():

    return {

        "a":

        test_request(

            "email/password json",

            {

                "email":
                    CLICKTRANS_EMAIL,

                "password":
                    CLICKTRANS_PASSWORD
            }

        ),

        "b":

        test_request(

            "username/password json",

            {

                "username":
                    CLICKTRANS_EMAIL,

                "password":
                    CLICKTRANS_PASSWORD
            }

        ),

        "c":

        test_request(

            "_username/_password json",

            {

                "_username":
                    CLICKTRANS_EMAIL,

                "_password":
                    CLICKTRANS_PASSWORD
            }

        ),

        "d":

        test_request(

            "email/password form",

            {

                "email":
                    CLICKTRANS_EMAIL,

                "password":
                    CLICKTRANS_PASSWORD
            },

            False
        )

    }


@app.post(
    "/webhook/new-auction"
)
async def new_auction(
    data: dict
):

    print(data)

    return {
        "ok": True
    }


@app.post(
    "/webhook/update-auction"
)
async def update_auction(
    data: dict
):

    return {
        "ok": True
    }