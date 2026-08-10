import tkinter as tk

from login_window import LoginWindow


def login_success(user):

    print("=" * 50)

    print("LOGIN BERHASIL")

    print(

        "Username :",

        user["username"]

    )

    print(

        "Role     :",

        user["role"]

    )

    print("=" * 50)


if __name__ == "__main__":

    app = LoginWindow(

        on_login_success=login_success

    )

    app.run()