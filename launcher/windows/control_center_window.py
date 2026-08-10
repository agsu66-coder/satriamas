import os
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog

from PIL import Image, ImageTk

from services.branding_service import branding_service
from services.permission_service import permission_service
from windows.user_management_window import UserManagementWindow


class ControlCenterWindow:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        parent,
        current_user
    ):

        self.parent = parent
        self.current_user = current_user

        # ==================================================
        # BRANDING
        # ==================================================

        self.branding = (
            branding_service
            .get_branding()
        )

        self.theme = (
            branding_service
            .get_theme()
        )

        self.application = (
            branding_service
            .get_application()
        )

        # ==================================================
        # THEME
        # ==================================================

        self.primary_color = (
            self.theme.get(
                "primary_color",
                "#12372A"
            )
        )

        self.accent_color = (
            self.theme.get(
                "accent_color",
                "#2D6A4F"
            )
        )

        self.background_color = (
            self.theme.get(
                "background_color",
                "#F3F5F6"
            )
        )

        self.card_color = (
            self.theme.get(
                "card_color",
                "#FFFFFF"
            )
        )

        self.text_color = (
            self.theme.get(
                "text_color",
                "#12372A"
            )
        )

        self.muted_color = "#64748B"

        # ==================================================
        # LOGO PREVIEW
        # ==================================================

        self.logo_preview_image = None
        # ==================================================
        # WINDOW
        # ==================================================

        self.window = tk.Toplevel(
            self.parent
        )

        self.window.title(
            "PUSAT KENDALI - "
            + self.branding.get(
                "system_name",
                "SATRIA MAS"
            )
        )

        self.window.geometry(
            "900x700"
        )

        self.window.minsize(
            750,
            550
        )

        self.window.configure(
            bg=self.background_color
        )

        self.window.transient(
            self.parent
        )

        # ==================================================
        # BUILD
        # ==================================================

        self.build_ui()

        self.load_values()

    # ==================================================
    # PERMISSION
    # ==================================================

    def has_permission(
        self,
        permission
    ):

        try:

            role = (
                self.current_user.get(
                    "role",
                    "USER"
                )
            )

            return (
                permission_service
                .can(
                    role,
                    permission
                )
            )

        except Exception as error:

            print(
                "[CONTROL CENTER PERMISSION ERROR]",
                error
            )

            return False

    # ==================================================
    # BUILD UI
    # ==================================================

    def build_ui(self):

        # ==================================================
        # HEADER
        # ==================================================

        header = tk.Frame(
            self.window,
            bg=self.primary_color,
            height=100
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        header_content = tk.Frame(
            header,
            bg=self.primary_color
        )

        header_content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        tk.Label(
            header_content,
            text="⚙  PUSAT KENDALI",
            font=(
                "Arial",
                20,
                "bold"
            ),
            fg="white",
            bg=self.primary_color
        ).pack(
            anchor="w"
        )

        tk.Label(
            header_content,
            text=(
                "Konfigurasi dan identitas "
                "SATRIA MAS"
            ),
            font=(
                "Arial",
                9
            ),
            fg="#D1FAE5",
            bg=self.primary_color
        ).pack(
            anchor="w"
        )

        # ==================================================
        # MAIN
        # ==================================================

        main = tk.Frame(
            self.window,
            bg=self.background_color
        )

        main.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # CANVAS
        # ==================================================

        self.canvas = tk.Canvas(
            main,
            bg=self.background_color,
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            main,
            orient="vertical",
            command=self.canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=self.background_color
        )

        self.canvas_window = (
            self.canvas.create_window(
                (0, 0),
                window=self.scrollable_frame,
                anchor="nw"
            )
        )

        self.scrollable_frame.bind(
            "<Configure>",
            self.on_frame_configure
        )

        self.canvas.bind(
            "<Configure>",
            self.on_canvas_configure
        )

        # ==================================================
        # SECTIONS
        # ==================================================

        self.build_branding_section()

        self.build_theme_section()

        self.build_application_section()

        self.build_user_management_section()

        self.build_footer()

    # ==================================================
    # SCROLL
    # ==================================================

    def on_frame_configure(
        self,
        event=None
    ):

        self.canvas.configure(
            scrollregion=self.canvas.bbox(
                "all"
            )
        )

    def on_canvas_configure(
        self,
        event
    ):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # ==================================================
    # BRANDING SECTION
    # ==================================================

    def build_branding_section(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=25,
            pady=25
        )

        tk.Label(
            section,
            text="IDENTITAS APLIKASI",
            font=(
                "Arial",
                16,
                "bold"
            ),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        card = tk.Frame(
            section,
            bg=self.card_color,
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )

        card.pack(
            fill="x"
        )

        content = tk.Frame(
            card,
            bg=self.card_color
        )

        content.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.branding_entries = {}

        fields = [
            (
                "system_name",
                "Nama Sistem"
            ),
            (
                "institution_name",
                "Nama Instansi"
            ),
            (
                "header_title",
                "Judul Header"
            ),
            (
                "header_description",
                "Deskripsi Header"
            ),
            (
                "footer_text",
                "Footer"
            )

        ]

        for key, label_text in fields:

            row = tk.Frame(
                content,
                bg=self.card_color
            )

            row.pack(
                fill="x",
                pady=5
            )

            tk.Label(
                row,
                text=label_text,
                width=22,
                anchor="w",
                font=(
                    "Arial",
                    9,
                    "bold"
                ),
                fg=self.text_color,
                bg=self.card_color
            ).pack(
                side="left"
            )

            entry = tk.Entry(
                row,
                font=(
                    "Arial",
                    10
                )
            )

            entry.pack(
                side="left",
                fill="x",
                expand=True
            )

            self.branding_entries[key] = entry

        # ==================================================
        # LOGO
        # ==================================================

        logo_row = tk.Frame(
            content,
            bg=self.card_color
        )

        logo_row.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            logo_row,
            text="Logo",
            width=22,
            anchor="w",
            font=(
                "Arial",
                9,
                "bold"
            ),
            fg=self.text_color,
            bg=self.card_color
        ).pack(
            side="left"
        )

        self.logo_entry = tk.Entry(
            logo_row,
            font=(
                "Arial",
                10
            )
        )

        self.logo_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        if self.has_permission(
            "EDIT_BRANDING"
        ):

            tk.Button(
                logo_row,
                text="Pilih Logo",
                command=self.choose_logo,
                relief="flat",
                cursor="hand2"
            ).pack(
                side="left",
                padx=(8, 0)
            )

        # ==================================================
        # LOGO PREVIEW
        # ==================================================

        preview_container = tk.Frame(
            content,
            bg=self.card_color
        )

        preview_container.pack(
            fill="x",
            pady=(15, 5)
        )

        tk.Label(
            preview_container,
            text="Preview Logo",
            font=(
                "Arial",
                9,
                "bold"
            ),
            fg=self.text_color,
            bg=self.card_color
        ).pack(
            anchor="w"
        )

        self.logo_preview_label = tk.Label(
            preview_container,
            text="Belum ada logo",
            font=(
                "Arial",
                9
            ),
            fg=self.muted_color,
            bg=self.card_color,
            width=20,
            height=6
        )

        self.logo_preview_label.pack(
            anchor="w",
            pady=(5, 5)
        )

        tk.Label(
            preview_container,
            text=(
                "Format yang didukung: PNG, JPG/JPEG, GIF, "
                "BMP, dan WEBP. Disarankan menggunakan PNG "
                "dengan latar transparan untuk hasil terbaik."
            ),
            font=(
                "Arial",
                8
            ),
            fg=self.muted_color,
            bg=self.card_color,
            justify="left",
            wraplength=650
        ).pack(
            anchor="w"
        )

        # ==================================================
        # SAVE BUTTON
        # ==================================================

        button_frame = tk.Frame(
            content,
            bg=self.card_color
        )

        button_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        if self.has_permission(
            "EDIT_BRANDING"
        ):

            tk.Button(
                button_frame,
                text="💾  SIMPAN IDENTITAS",
                command=self.save_branding,
                font=(
                    "Arial",
                    10,
                    "bold"
                ),
                fg="white",
                bg=self.accent_color,
                activebackground=self.primary_color,
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8
            ).pack(
                side="right"
            )

        else:

            tk.Label(
                button_frame,
                text=(
                    "Anda tidak memiliki hak "
                    "untuk mengubah identitas."
                ),
                font=(
                    "Arial",
                    9
                ),
                fg=self.muted_color,
                bg=self.card_color
            ).pack(
                side="right"
            )

    # ==================================================
    # THEME SECTION
    # ==================================================

    def build_theme_section(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        tk.Label(
            section,
            text="TEMA APLIKASI",
            font=(
                "Arial",
                16,
                "bold"
            ),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        card = tk.Frame(
            section,
            bg=self.card_color,
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )

        card.pack(
            fill="x"
        )

        content = tk.Frame(
            card,
            bg=self.card_color
        )

        content.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.theme_entries = {}

        fields = [
            (
                "primary_color",
                "Primary Color"
            ),
            (
                "accent_color",
                "Accent Color"
            ),
            (
                "background_color",
                "Background Color"
            ),
            (
                "card_color",
                "Card Color"
            ),
            (
                "text_color",
                "Text Color"
            )
        ]

        for key, label_text in fields:

            row = tk.Frame(
                content,
                bg=self.card_color
            )

            row.pack(
                fill="x",
                pady=5
            )

            tk.Label(
                row,
                text=label_text,
                width=22,
                anchor="w",
                font=(
                    "Arial",
                    9,
                    "bold"
                ),
                fg=self.text_color,
                bg=self.card_color
            ).pack(
                side="left"
            )

            entry = tk.Entry(
                row,
                font=(
                    "Arial",
                    10
                )
            )

            entry.pack(
                side="left",
                fill="x",
                expand=True
            )

            self.theme_entries[key] = entry

            tk.Button(
                row,
                text="Pilih",
                command=lambda e=entry: self.choose_color(e),
                relief="flat",
                cursor="hand2"
            ).pack(
                side="left",
                padx=(8, 0)
            )

        if self.has_permission(
            "EDIT_THEME"
        ):

            tk.Button(
                content,
                text="🎨  SIMPAN TEMA",
                command=self.save_theme,
                font=(
                    "Arial",
                    10,
                    "bold"
                ),
                fg="white",
                bg=self.accent_color,
                activebackground=self.primary_color,
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8
            ).pack(
                anchor="e",
                pady=(15, 0)
            )

        else:

            tk.Label(
                content,
                text=(
                    "Anda tidak memiliki hak "
                    "untuk mengubah tema."
                ),
                font=(
                    "Arial",
                    9
                ),
                fg=self.muted_color,
                bg=self.card_color
            ).pack(
                anchor="e",
                pady=(15, 0)
            )

    # ==================================================
    # APPLICATION SECTION
    # ==================================================

    def build_application_section(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        tk.Label(
            section,
            text="INFORMASI APLIKASI",
            font=(
                "Arial",
                16,
                "bold"
            ),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        card = tk.Frame(
            section,
            bg=self.card_color,
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )

        card.pack(
            fill="x"
        )

        content = tk.Frame(
            card,
            bg=self.card_color
        )

        content.pack(
            fill="x",
            padx=20,
            pady=20
        )

        values = [
            (
                "Versi",
                self.application.get(
                    "version",
                    "-"
                )
            ),
            (
                "Environment",
                self.application.get(
                    "environment",
                    "-"
                )
            ),
            (
                "Konfigurasi",
                branding_service.get_status().get(
                    "path",
                    "-"
                )
            )
        ]

        for label_text, value in values:

            row = tk.Frame(
                content,
                bg=self.card_color
            )

            row.pack(
                fill="x",
                pady=4
            )

            tk.Label(
                row,
                text=label_text,
                width=22,
                anchor="w",
                font=(
                    "Arial",
                    9,
                    "bold"
                ),
                fg=self.text_color,
                bg=self.card_color
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text=str(value),
                anchor="w",
                fg=self.muted_color,
                bg=self.card_color
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

    # ==================================================
    # USER MANAGEMENT SECTION
    # ==================================================

    def build_user_management_section(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        tk.Label(
            section,
            text="MANAJEMEN PENGGUNA",
            font=(
                "Arial",
                16,
                "bold"
            ),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        card = tk.Frame(
            section,
            bg=self.card_color,
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )

        card.pack(
            fill="x"
        )

        content = tk.Frame(
            card,
            bg=self.card_color
        )

        content.pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            content,
            text=(
                "Kelola akun pengguna dan hak akses "
                "SATRIA MAS."
            ),
            font=(
                "Arial",
                9
            ),
            fg=self.muted_color,
            bg=self.card_color,
            justify="left"
        ).pack(
            anchor="w"
        )

        if self.has_permission("MANAGE_USERS"):

            tk.Button(
                content,
                text="👥  USER MANAGEMENT",
                command=self.open_user_management,
                font=(
                    "Arial",
                    10,
                    "bold"
                ),
                fg="white",
                bg=self.accent_color,
                activebackground=self.primary_color,
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                padx=15,
                pady=8
            ).pack(
                anchor="e",
                pady=(15, 0)
            )

        else:

            tk.Label(
                content,
                text=(
                    "Anda tidak memiliki hak "
                    "untuk mengelola pengguna."
                ),
                font=(
                    "Arial",
                    9
                ),
                fg=self.muted_color,
                bg=self.card_color
            ).pack(
                anchor="e",
                pady=(15, 0)
            )

    # ==================================================
    # OPEN USER MANAGEMENT
    # ==================================================

    def open_user_management(self):

        if not self.has_permission(
            "MANAGE_USERS"
        ):

            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki hak "
                "untuk mengelola pengguna."
            )

            return

        try:

            UserManagementWindow(
                self.window,
                current_user=self.current_user
            )

        except Exception as error:

            messagebox.showerror(
                "User Management",
                "Gagal membuka User Management.\n\n"
                + str(error)
            )

    # ==================================================
    # FOOTER
    # ==================================================

    def build_footer(self):

        footer = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        footer.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        tk.Frame(
            footer,
            bg="#CBD5E1",
            height=1
        ).pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            footer,
            text="Pusat Kendali SATRIA MAS",
            font=(
                "Arial",
                9
            ),
            fg=self.muted_color,
            bg=self.background_color
        ).pack()

    # ==================================================
    # LOAD VALUES
    # ==================================================

    def load_values(self):

        branding = (
            branding_service
            .get_branding()
        )

        theme = (
            branding_service
            .get_theme()
        )

        for key, entry in self.branding_entries.items():

            entry.delete(
                0,
                "end"
            )

            entry.insert(
                0,
                str(
                    branding.get(
                        key,
                        ""
                    )
                )
            )

        # ==================================================
        # LOAD LOGO
        # ==================================================

        logo_path = branding.get(
            "logo",
            ""
        )

        self.logo_entry.delete(
            0,
            "end"
        )

        self.logo_entry.insert(
            0,
            str(
                logo_path
            )
        )

        self.load_logo_preview(
            logo_path
        )

        for key, entry in self.theme_entries.items():

            entry.delete(
                0,
                "end"
            )

            entry.insert(
                0,
                str(
                    theme.get(
                        key,
                        ""
                    )
                )
            )

    # ==================================================
    # CHOOSE LOGO
    # ==================================================

    def choose_logo(self):

        if not self.has_permission(
            "EDIT_BRANDING"
        ):

            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki hak "
                "untuk mengubah logo."
            )

            return

        file_path = filedialog.askopenfilename(

            parent=self.window,

            title="Pilih File Logo",

            filetypes=[
                (
                    "File Logo",
                    "*.png *.jpg *.jpeg *.gif *.bmp *.webp"
                ),
                (
                    "PNG",
                    "*.png"
                ),
                (
                    "JPEG",
                    "*.jpg *.jpeg"
                ),
                (
                    "GIF",
                    "*.gif"
                ),
                (
                    "BMP",
                    "*.bmp"
                ),
                (
                    "WEBP",
                    "*.webp"
                )

            ]

        )

        if not file_path:

            return

        try:

            image = Image.open(
                file_path
            )

            image.verify()

            # Buka kembali karena verify()
            # membuat image object tidak dapat
            # digunakan untuk proses berikutnya.
            image = Image.open(
                file_path
            )

            image.load()

        # ==========================================
        # KONVERSI KE PNG
        # ==========================================

            if image.mode in ("RGBA", "LA", "P"):
                image = image.convert("RGBA")

            else:
                image = image.convert("RGB")

        # ==========================================
        # FOLDER ASSETS
        # ==========================================

            base_dir = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(
                        branding_service.config_path
                    )
                )
            )

            assets_dir = os.path.join(
                base_dir,
                "assets"
            )

            os.makedirs(
                assets_dir,
                exist_ok=True
            )

            target_path = os.path.join(
                assets_dir,
                "logo.png"
            )

            # ==========================================
            # SIMPAN LOGO
            # ==========================================

            image.save(
                target_path,
                "PNG"
            )

            # ==========================================
            # PATH RELATIF
            # ==========================================

            relative_path = os.path.relpath(
            target_path,
            base_dir
            ).replace(
                os.sep,
                "/"
            )

        # ==========================================
        # PREVIEW
        # ==========================================

            preview = image.copy()

            preview.thumbnail(
                (
                    120,
                    120
                )
            )

            self.logo_preview_image = ImageTk.PhotoImage(
                preview
            )

            self.logo_preview_label.configure(
                image=self.logo_preview_image,
                text=""
            )

        # ==========================================
        # ISI ENTRY
        # ==========================================

            self.logo_entry.delete(
                0,
                "end"
            )

            self.logo_entry.insert(
                0,
                relative_path
            )

            messagebox.showinfo(
                "Logo",
                "Logo berhasil dipilih dan disiapkan "
                "untuk digunakan oleh aplikasi."
            )

        except Exception as error:

            messagebox.showerror(
                "Logo Tidak Valid",
                (
                    "File yang dipilih tidak dapat "
                    "digunakan sebagai logo.\n\n"
                    f"Detail: {error}"
                )
            )
    # ==================================================
    # LOAD LOGO PREVIEW
    # ==================================================

    def load_logo_preview(
        self,
        logo_path
    ):

        if not logo_path:

            self.logo_preview_label.configure(
                image="",
                text="Belum ada logo"
            )

            self.logo_preview_image = None

            return

        try:

            if not os.path.isabs(
                logo_path
            ):

                base_dir = os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(
                            branding_service.config_path
                        )
                    )
                )

                logo_path = os.path.join(
                    base_dir,
                    logo_path
                )

            if not os.path.exists(
                logo_path
            ):

                self.logo_preview_label.configure(
                    image="",
                    text="Logo tidak ditemukan"
                )

                self.logo_preview_image = None

                return

            image = Image.open(
                logo_path
            )

            image.thumbnail(
                (
                    120,
                    120
                )
            )

            self.logo_preview_image = ImageTk.PhotoImage(
                image
            )

            self.logo_preview_label.configure(
                image=self.logo_preview_image,
                text=""
            )

        except Exception as error:

            print(
                "[CONTROL CENTER] "
                "Gagal memuat preview logo:",
                error
            )

            self.logo_preview_label.configure(
                image="",
                text="Preview tidak tersedia"
            )

            self.logo_preview_image = None
    # ==================================================
    # SAVE BRANDING
    # ==================================================

    def save_branding(self):

        if not self.has_permission(
            "EDIT_BRANDING"
        ):

            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki hak untuk mengubah identitas."
            )

            return

        try:

            for key, entry in self.branding_entries.items():

                value = (
                    entry.get()
                    .strip()
                )

                branding_service.update_branding(
                    key,
                    value
                )

            # ==========================================
            # SAVE LOGO
            # ==========================================

            logo_path = (
                self.logo_entry
                .get()
                .strip()
            )

            if logo_path:

                if not os.path.isabs(
                    logo_path
                ):

                    base_dir = os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(
                                branding_service.config_path
                            )
                        )
                    )

                    full_logo_path = os.path.join(
                        base_dir,
                        logo_path
                    )

                else:

                    full_logo_path = logo_path

                if not os.path.exists(
                    full_logo_path
                ):

                    messagebox.showwarning(
                        "Logo Tidak Ditemukan",
                        (
                            "Path logo tidak ditemukan:\n\n"
                            f"{full_logo_path}\n\n"
                            "Silakan pilih file logo yang valid."
                        )
                    )

                    return

            branding_service.update_branding(
                "logo",
                logo_path
            )

            messagebox.showinfo(
                "Pusat Kendali",
                "Identitas aplikasi berhasil disimpan.\n\n"
                "Perubahan akan digunakan oleh window "
                "yang membaca branding_service."
            )

        except Exception as error:

            messagebox.showerror(
                "Gagal Menyimpan",
                str(error)
            )

    # ==================================================
    # SAVE THEME
    # ==================================================

    def save_theme(self):

        if not self.has_permission(
            "EDIT_THEME"
        ):

            messagebox.showerror(
                "Akses Ditolak",
                "Anda tidak memiliki hak untuk mengubah tema."
            )

            return

        try:

            for key, entry in self.theme_entries.items():

                value = (
                    entry.get()
                    .strip()
                )

                branding_service.update_theme(
                    key,
                    value
                )

            messagebox.showinfo(
                "Pusat Kendali",
                "Tema aplikasi berhasil disimpan."
            )

        except Exception as error:

            messagebox.showerror(
                "Gagal Menyimpan",
                str(error)
            )

    # ==================================================
    # COLOR PICKER
    # ==================================================

    def choose_color(
        self,
        entry
    ):

        current = (
            entry.get()
            .strip()
        )

        try:

            result = colorchooser.askcolor(
                color=current
            )

        except Exception:

            result = colorchooser.askcolor()

        if result and result[1]:

            entry.delete(
                0,
                "end"
            )

            entry.insert(
                0,
                result[1]
            )

    # ==================================================
    # RUN
    # ==================================================

    def run(self):

        self.window.grab_set()

        self.window.focus_force()