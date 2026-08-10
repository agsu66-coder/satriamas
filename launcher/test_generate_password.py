from services.auth_service import auth_service


passwords = {

    "superadmin": "superadmin123",

    "admin": "admin123",

    "operator": "operator123"

}


for username, password in passwords.items():

    auth_service.create_user(

        username,

        password,

        {

            "superadmin": "SUPERADMIN",

            "admin": "ADMIN",

            "operator": "USER"

        }[username]

    )


print(

    "User berhasil dibuat."

)