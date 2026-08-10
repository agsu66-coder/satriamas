import tkinter as tk
from tkinter import messagebox

from services.auth_service import auth_service


class LoginWindow:

    def __init__(self, on_login_success):

        self.on_login_success = on_login_success

        self.root = tk.Tk()

        self.root.title(
            "SATRIA MAS BINANGUN - Login"
        )

        self.root.geometry(
            "500x420"
        )

        self.root.resizable(
            False,
            False
        )

        self.build_ui()

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        # ==============================
        # HEADER
        # ==============================

        header = tk.Frame(

            self.root,

            bg="#1B5E20",

            height=120

        )

        header.pack(

            fill="x"

        )

        header.pack_propagate(

            False

        )


        title = tk.Label(

            header,

            text="SATRIA MAS",

            font=(

                "Broadway",

                24,

                "bold"

            ),

            fg="white",

            bg="#1B5E20"

        )

        title.pack(

            pady=(22, 0)

        )


        subtitle = tk.Label(

            header,

            text="Sarana Informasi Terpadu dan Aduan Masyarakat",

            font=(

                "Segoe UI",

                10

            ),

            fg="#C8E6C9",

            bg="#1B5E20"

        )

        subtitle.pack()


        # ==============================
        # LOGIN AREA
        # ==============================

        body = tk.Frame(

            self.root,

            bg="#F5F7F6"

        )

        body.pack(

            fill="both",

            expand=True

        )


        login_frame = tk.Frame(

            body,

            bg="white",

            padx=35,

            pady=25

        )

        login_frame.place(

            relx=0.5,

            rely=0.5,

            anchor="center"

        )


        title_login = tk.Label(

            login_frame,

            text="LOGIN SYSTEM",

            font=(

                "Segoe UI",

                14,

                "bold"

            ),

            bg="white",

            fg="#263238"

        )

        title_login.pack(

            pady=(0, 20)

        )


        # USERNAME

        tk.Label(

            login_frame,

            text="Username",

            font=(

                "Segoe UI",

                10,

                "bold"

            ),

            bg="white",

            anchor="w"

        ).pack(

            fill="x"

        )


        self.username_entry = tk.Entry(

            login_frame,

            font=(

                "Segoe UI",

                11

            ),

            width=30

        )

        self.username_entry.pack(

            pady=(5, 15)

        )


        # PASSWORD

        tk.Label(

            login_frame,

            text="Password",

            font=(

                "Segoe UI",

                10,

                "bold"

            ),

            bg="white",

            anchor="w"

        ).pack(

            fill="x"

        )


        self.password_entry = tk.Entry(

            login_frame,

            font=(

                "Segoe UI",

                11

            ),

            width=30,

            show="•"

        )

        self.password_entry.pack(

            pady=(5, 20)

        )


        # LOGIN BUTTON

        login_button = tk.Button(

            login_frame,

            text="🔐  LOGIN",

            font=(

                "Segoe UI",

                11,

                "bold"

            ),

            bg="#2E7D32",

            fg="white",

            activebackground="#1B5E20",

            activeforeground="white",

            width=25,

            height=2,

            relief="flat",

            command=self.login

        )

        login_button.pack()


        # ENTER

        self.root.bind(

            "<Return>",

            lambda event: self.login()

        )


        self.username_entry.focus()


    # ==========================================
    # LOGIN
    # ==========================================

    def login(self):

        username = (

            self.username_entry

            .get()

            .strip()

        )


        password = (

            self.password_entry

            .get()

        )


        if not username:

            messagebox.showwarning(

                "Login",

                "Username wajib diisi."

            )

            return


        if not password:

            messagebox.showwarning(

                "Login",

                "Password wajib diisi."

            )

            return


        result = auth_service.login(

            username,

            password

        )


        if not result.get(

            "success"

        ):

            messagebox.showerror(

                "Login Gagal",

                result.get(

                    "message",

                    "Login gagal."

                )

            )

            return


        user = result.get(

            "user"

        )


        self.root.destroy()


        self.on_login_success(

            user

        )


    # ==========================================
    # RUN
    # ==========================================

    def run(self):

        self.root.mainloop()