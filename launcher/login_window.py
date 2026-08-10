import os
import tkinter as tk
from tkinter import messagebox

from services.auth_service import auth_service
from services.branding_service import branding_service


class LoginWindow:

    def __init__(self, parent, on_login_success):

        self.on_login_success = on_login_success

        # ==========================================
        # BRANDING
        # ==========================================

        self.branding = branding_service.get_branding()
        self.theme = branding_service.get_theme()

        self.system_name = self.branding.get(
            "system_name",
            "SATRIA MAS BINANGUN"
        )

        self.institution_name = self.branding.get(
            "institution_name",
            ""
        )

        self.header_title = self.branding.get(
            "header_title",
            ""
        )

        self.header_description = self.branding.get(
            "header_description",
            ""
        )

        self.logo_path = self.branding.get(
            "logo",
            "assets/logo.png"
        )

        # ==========================================
        # THEME
        # ==========================================

        self.primary_color = self.theme.get(
            "primary_color",
            "#12372A"
        )

        self.accent_color = self.theme.get(
            "accent_color",
            "#2D6A4F"
        )

        self.background_color = self.theme.get(
            "background_color",
            "#F3F5F6"
        )

        self.card_color = self.theme.get(
            "card_color",
            "#FFFFFF"
        )

        self.text_color = self.theme.get(
            "text_color",
            "#12372A"
        )

        # ==========================================
        # WINDOW
        # ==========================================

        self.root = tk.Toplevel(parent)

        self.root.title(
            f"{self.system_name} - Login"
        )

        self.root.geometry(
            "500x420"
        )

        self.root.resizable(
            False,
            False
        )

        self.root.configure(
            bg=self.background_color
        )

        # Menyimpan reference image agar tidak
        # dihapus oleh garbage collector.
        self.logo_image = None

        self.build_ui()

    # ==========================================
    # RESOLVE LOGO PATH
    # ==========================================

    def get_logo_path(self):

        # branding_config.json berada di:
        #
        # config/branding_config.json
        #
        # base directory aplikasi berada satu tingkat
        # di atas folder config.

        config_dir = os.path.dirname(
            branding_service.config_path
        )

        base_dir = os.path.dirname(
            config_dir
        )

        logo_path = self.logo_path

        # Jika path absolut, langsung gunakan.
        if os.path.isabs(logo_path):

            return logo_path

        return os.path.join(
            base_dir,
            logo_path
        )

    # ==========================================
    # LOAD LOGO
    # ==========================================

    def load_logo(self):

        logo_path = self.get_logo_path()

        if not os.path.exists(logo_path):

            print(
                "[LOGIN] Logo tidak ditemukan:",
                logo_path
            )

            return None

        try:

            image = tk.PhotoImage(
                file=logo_path
            )

            # Skala sederhana jika logo terlalu besar.
            width = image.width()
            height = image.height()

            max_width = 130
            max_height = 130

            scale_x = max(
                1,
                (width + max_width - 1)
                // max_width
            )

            scale_y = max(
                1,
                (height + max_height - 1)
                // max_height
            )

            scale = max(
                scale_x,
                scale_y
            )

            if scale > 1:

                image = image.subsample(
                    scale,
                    scale
                )

            self.logo_image = image

            return image

        except Exception as error:

            print(
                "[LOGIN] Gagal memuat logo:",
                error
            )

            return None

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        # ==========================================
        # HEADER
        # ==========================================

        header = tk.Frame(

            self.root,

            bg=self.primary_color,

            height=120

        )

        header.pack(

            fill="x"

        )

        header.pack_propagate(

            False

        )

        # ==========================================
        # HEADER CONTENT
        # ==========================================

        header_content = tk.Frame(

            header,

            bg=self.primary_color

        )

        header_content.pack(

            fill="both",

            expand=True,

            padx=25

        )

        # ==========================================
        # LOGO
        # ==========================================

        logo = self.load_logo()

        if logo:

            logo_label = tk.Label(

                header_content,

                image=logo,

                bg=self.primary_color

            )

            logo_label.pack(

                side="left",

                padx=(0, 15)

            )

        # ==========================================
        # HEADER TEXT
        # ==========================================

        header_text = tk.Frame(

            header_content,

            bg=self.primary_color

        )

        header_text.pack(

            side="left",

            fill="both",

            expand=True

        )

        title = tk.Label(

            header_text,

            text=self.system_name,

            font=(

                "Broadway",

                24,

                "bold"

            ),

            fg="white",

            bg=self.primary_color

        )

        title.pack(

            anchor="w",

            pady=(18, 0)

        )

        # Prioritas:
        #
        # header_description
        # ↓
        # fallback header_title
        # ↓
        # fallback institution_name

        subtitle_text = (

            self.header_description

            or self.header_title

            or self.institution_name

            or "Sarana Informasi Terpadu dan Aduan Masyarakat"

        )

        subtitle = tk.Label(

            header_text,

            text=subtitle_text,

            font=(

                "Segoe UI",

                9

            ),

            fg="#D1FAE5",

            bg=self.primary_color,

            wraplength=330,

            justify="left"

        )

        subtitle.pack(

            anchor="w"

        )

        # ==========================================
        # LOGIN AREA
        # ==========================================

        body = tk.Frame(

            self.root,

            bg=self.background_color

        )

        body.pack(

            fill="both",

            expand=True

        )

        login_frame = tk.Frame(

            body,

            bg=self.card_color,

            padx=35,

            pady=25

        )

        login_frame.place(

            relx=0.5,

            rely=0.5,

            anchor="center"

        )

        # ==========================================
        # LOGIN TITLE
        # ==========================================

        title_login = tk.Label(

            login_frame,

            text="LOGIN SYSTEM",

            font=(

                "Segoe UI",

                14,

                "bold"

            ),

            bg=self.card_color,

            fg=self.text_color

        )

        title_login.pack(

            pady=(0, 20)

        )

        # ==========================================
        # USERNAME
        # ==========================================

        tk.Label(

            login_frame,

            text="Username",

            font=(

                "Segoe UI",

                10,

                "bold"

            ),

            bg=self.card_color,

            fg=self.text_color,

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

        # ==========================================
        # PASSWORD
        # ==========================================

        tk.Label(

            login_frame,

            text="Password",

            font=(

                "Segoe UI",

                10,

                "bold"

            ),

            bg=self.card_color,

            fg=self.text_color,

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

        # ==========================================
        # LOGIN BUTTON
        # ==========================================

        login_button = tk.Button(

            login_frame,

            text="🔐  LOGIN",

            font=(

                "Segoe UI",

                11,

                "bold"

            ),

            bg=self.accent_color,

            fg="white",

            activebackground=self.primary_color,

            activeforeground="white",

            width=25,

            height=2,

            relief="flat",

            cursor="hand2",

            command=self.login

        )

        login_button.pack()

        # ==========================================
        # ENTER
        # ==========================================

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
