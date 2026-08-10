import os
import json
import hashlib


class AuthService:

    def __init__(self):

        self.file_path = os.path.join(

            os.path.dirname(__file__),

            "..",

            "config",

            "users.json"

        )

        self.users = []

        self.load_users()

    # ==========================================
    # HASH PASSWORD
    # ==========================================

    def hash_password(self, password):

        return hashlib.sha256(

            password.encode("utf-8")

        ).hexdigest()

    # ==========================================
    # LOAD USERS
    # ==========================================

    def load_users(self):

        if not os.path.exists(

            self.file_path

        ):

            self.users = []

            return

        with open(

            self.file_path,

            "r",

            encoding="utf-8"

        ) as file:

            data = json.load(file)

        self.users = data.get(

            "users",

            []

        )

    # ==========================================
    # SIMPAN USERS
    # ==========================================

    def save_users(self):

        folder = os.path.dirname(

            self.file_path

        )

        os.makedirs(

            folder,

            exist_ok=True

        )

        with open(

            self.file_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                {

                    "users": self.users

                },

                file,

                indent=4

            )

    # ==========================================
    # LOGIN
    # ==========================================

    def login(self, username, password):

        if not username or not password:

            return {

                "success": False,

                "message": "Username dan password wajib diisi."

            }

        username = username.strip()

        password_hash = self.hash_password(

            password

        )

        for user in self.users:

            if (

                user.get("username")

                == username

            ):

                if not user.get(

                    "active",

                    False

                ):

                    return {

                        "success": False,

                        "message": "Akun tidak aktif."

                    }

                if user.get(

                    "password_hash"

                ) != password_hash:

                    return {

                        "success": False,

                        "message": "Password salah."

                    }

                return {

                    "success": True,

                    "message": "Login berhasil.",

                    "user": {

                        "username":

                            user.get(

                                "username"

                            ),

                        "role":

                            user.get(

                                "role"

                            )

                    }

                }

        return {

            "success": False,

            "message": "Username tidak ditemukan."

        }

    # ==========================================
    # CEK USERNAME
    # ==========================================

    def username_exists(self, username):

        return any(

            user.get("username")

            == username

            for user in self.users

        )

    # ==========================================
    # BUAT USER
    # ==========================================

    def create_user(

        self,

        username,

        password,

        role="USER"

    ):

        if self.username_exists(

            username

        ):

            return False

        user = {

            "username": username,

            "password_hash":

                self.hash_password(

                    password

                ),

            "role": role.upper(),

            "active": True

        }

        self.users.append(user)

        self.save_users()

        return True


auth_service = AuthService()