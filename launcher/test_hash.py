from services.auth_service import auth_service


print("=" * 60)
print("TEST HASH PASSWORD")
print("=" * 60)


passwords = {

    "superadmin": "superadmin123",

    "admin": "admin123",

    "operator": "operator123"

}


for username, password in passwords.items():

    print("\nUSERNAME :", username)

    print(
        "PASSWORD :",
        password
    )

    print(
        "HASH :",
        auth_service.hash_password(password)
    )


print("\n")

print("DATA USERS")

for user in auth_service.users:

    print(user)