import requests

BASE = "http://127.0.0.1:5000"

print("=" * 40)
print("TEST TEMPLATE API")
print("=" * 40)

# ----------------------------

print("\nGET TEMPLATE")

r = requests.get(

    BASE + "/template/WELCOME"

)

print(r.json())

# ----------------------------

print("\nLIST")

r = requests.get(

    BASE + "/template/list"

)

print(r.json())

# ----------------------------

print("\nRENDER")

r = requests.post(

    BASE + "/template/render",

    json={

        "key": "WELCOME",

        "data": {

            "nama": "Administrator"

        }

    }

)

print(r.json())

# ----------------------------

print("\nRELOAD")

r = requests.post(

    BASE + "/template/reload"

)

print(r.json())