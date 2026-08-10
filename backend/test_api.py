"""
==================================================
TERATAI AI

API Integration Test
Version : 1.0.0

Menguji seluruh endpoint REST API.

==================================================
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


# ==================================================
# PRINT
# ==================================================

def print_result(title, response):

    print("=" * 60)
    print(title)

    try:
        print(response.json())
    except Exception:
        print(response.text)


# ==================================================
# HOME
# ==================================================

def test_home():

    response = requests.get(
        f"{BASE_URL}/"
    )

    print_result(
        "GET /",
        response
    )


# ==================================================
# HEALTH
# ==================================================

def test_health():

    response = requests.get(
        f"{BASE_URL}/health"
    )

    print_result(
        "GET /health",
        response
    )


# ==================================================
# ASK
# ==================================================

def test_ask(question):

    response = requests.post(

        f"{BASE_URL}/ask",

        json={
            "query": question
        }

    )

    print_result(
        f"POST /ask : {question}",
        response
    )


# ==================================================
# TEMPLATE LIST
# ==================================================

def test_template_list():

    response = requests.get(

        f"{BASE_URL}/template/list"

    )

    print_result(
        "GET /template/list",
        response
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    test_home()

    test_health()

    test_template_list()

    test_ask("Halo")

    test_ask("Bagaimana cara membuat KTP baru?")

    test_ask("Saya ingin membuat KTP")

    test_ask("Mengurus kartu keluarga")

    test_ask("Saya kehilangan dompet")