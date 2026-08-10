import tkinter as tk
from tkinter import messagebox, ttk

from services.auth_service import auth_service
from services.permission_service import permission_service


class UserManagementWindow:

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
        # WINDOW
        # ==================================================

        self.window = tk.Toplevel(
            self.parent
        )

        self.window.title(
            "MANAJEMEN PENGGUNA"
        )

        self.window.geometry(
            "1100x720"
        )

        self.window.minsize(
            950,
            620
        )

        self.window.configure(
            bg="#F3F5F6"
        )

        self.window.transient(
            self.parent
        )

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        # ==================================================
        # STATE
        # ==================================================

        self.selected_username = None

        self.user_list = []

        self.form_mode = None
        # None
        # CREATE
        # EDIT

        self.role_var = tk.StringVar(
            value="USER"
        )

        self.active_var = tk.BooleanVar(
            value=True
        )

        self.password_var = tk.StringVar()

        self.password_visible = False

        # ==================================================
        # STYLE
        # ==================================================

        self.configure_styles()

        # ==================================================
        # BUILD
        # ==================================================

        self.build_ui()

        self.load_users()

        self.hide_user_form()

    # ==================================================
    # STYLE
    # ==================================================

    def configure_styles(self):

        style = ttk.Style()

        try:
            style.theme_use(
                "clam"
            )
        except Exception:
            pass

        style.configure(
            "User.Treeview",
            background="#F8FAFC",
            foreground="#12372A",
            rowheight=30,
            fieldbackground="#F8FAFC",
            font=(
                "Arial",
                9
            )
        )

        style.configure(
            "User.Treeview.Heading",
            background="#12372A",
            foreground="white",
            font=(
                "Arial",
                9,
                "bold"
            ),
            padding=7
        )

        style.map(
            "User.Treeview",
            background=[
                (
                    "selected",
                    "#2D7D5B"
                )
            ],
            foreground=[
                (
                    "selected",
                    "white"
                )
            ]
        )

    # ==================================================
    # PERMISSION
    # ==================================================

    def has_permission(
        self,
        permission
    ):

        try:

            role = str(
                self.current_user.get(
                    "role",
                    "USER"
                )
            ).upper()

            return (
                permission_service.can(
                    role,
                    permission
                )
            )

        except Exception as error:

            print(
                "[USER MANAGEMENT PERMISSION ERROR]",
                error
            )

            return False

    # ==================================================
    # ACCESS VALIDATION
    # ==================================================

    def check_access(self):

        role = str(
            self.current_user.get(
                "role",
                "USER"
            )
        ).upper()

        return (
            role == "SUPERADMIN"
            and
            self.has_permission(
                "MANAGE_USERS"
            )
        )

    # ==================================================
    # BUILD UI
    # ==================================================

    def build_ui(self):

        # ==================================================
        # HEADER
        # ==================================================

        header = tk.Frame(
            self.window,
            bg="#12372A",
            height=105
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        header_content = tk.Frame(
            header,
            bg="#12372A"
        )

        header_content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        tk.Label(
            header_content,
            text="👥  MANAJEMEN PENGGUNA",
            font=(
                "Arial",
                20,
                "bold"
            ),
            fg="white",
            bg="#12372A"
        ).pack(
            anchor="w"
        )

        tk.Label(
            header_content,
            text=(
                "Kelola akun, role, dan status pengguna "
                "SATRIA MAS"
            ),
            font=(
                "Arial",
                9
            ),
            fg="#D1FAE5",
            bg="#12372A"
        ).pack(
            anchor="w"
        )

        # ==================================================
        # MAIN
        # ==================================================

        main = tk.Frame(
            self.window,
            bg="#F3F5F6"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ==================================================
        # LEFT PANEL
        # ==================================================

        left = tk.Frame(
            main,
            bg="#FFFFFF",
            highlightbackground="#CBD5E1",
            highlightthickness=1,
            width=430
        )

        left.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        left.pack_propagate(
            False
        )

        tk.Label(
            left,
            text="DAFTAR PENGGUNA",
            font=(
                "Arial",
                14,
                "bold"
            ),
            fg="#12372A",
            bg="#FFFFFF"
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # ==================================================
        # USER TABLE
        # ==================================================

        table_frame = tk.Frame(
            left,
            bg="#FFFFFF"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        self.user_table = ttk.Treeview(
            table_frame,
            columns=(
                "username",
                "role",
                "status"
            ),
            show="headings",
            style="User.Treeview",
            selectmode="browse"
        )

        self.user_table.heading(
            "username",
            text="USERNAME"
        )

        self.user_table.heading(
            "role",
            text="ROLE"
        )

        self.user_table.heading(
            "status",
            text="STATUS"
        )

        self.user_table.column(
            "username",
            width=160,
            anchor="w"
        )

        self.user_table.column(
            "role",
            width=130,
            anchor="center"
        )

        self.user_table.column(
            "status",
            width=90,
            anchor="center"
        )

        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.user_table.yview
        )

        self.user_table.configure(
            yscrollcommand=table_scrollbar.set
        )

        self.user_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        table_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.user_table.bind(
            "<<TreeviewSelect>>",
            self.on_user_selected
        )

        # ==================================================
        # LEFT BUTTONS
        # ==================================================

        button_frame = tk.Frame(
            left,
            bg="#FFFFFF"
        )

        button_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.add_button = tk.Button(
            button_frame,
            text="+  TAMBAH USER",
            command=self.show_create_form,
            font=(
                "Arial",
                9,
                "bold"
            ),
            fg="white",
            bg="#2D7D5B",
            activebackground="#246A4C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=8
        )

        self.add_button.pack(
            fill="x",
            pady=3
        )

        self.edit_button = tk.Button(
            button_frame,
            text="✎  UBAH",
            command=self.show_edit_form,
            font=(
                "Arial",
                9,
                "bold"
            ),
            fg="white",
            bg="#2563EB",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=8,
            state="disabled"
        )

        self.edit_button.pack(
            fill="x",
            pady=3
        )

        self.refresh_button = tk.Button(
            button_frame,
            text="↻  REFRESH",
            command=self.load_users,
            font=(
                "Arial",
                9,
                "bold"
            ),
            fg="white",
            bg="#607D8B",
            activebackground="#455A64",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=8
        )

        self.refresh_button.pack(
            fill="x",
            pady=3
        )

        # ==================================================
        # RIGHT PANEL
        # ==================================================

        self.right = tk.Frame(
            main,
            bg="#FFFFFF",
            highlightbackground="#CBD5E1",
            highlightthickness=1
        )

        self.right.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # EMPTY STATE
        # ==================================================

        self.empty_state = tk.Frame(
            self.right,
            bg="#FFFFFF"
        )

        self.empty_state.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            self.empty_state,
            text="DATA PENGGUNA",
            font=(
                "Arial",
                16,
                "bold"
            ),
            fg="#12372A",
            bg="#FFFFFF"
        ).pack(
            pady=(150, 10)
        )

        tk.Label(
            self.empty_state,
            text=(
                "Pilih pengguna kemudian klik UBAH,\n"
                "atau klik TAMBAH USER untuk membuat "
                "pengguna baru."
            ),
            font=(
                "Arial",
                10
            ),
            fg="#64748B",
            bg="#FFFFFF",
            justify="center"
        ).pack()

        # ==================================================
        # FORM CONTAINER
        # ==================================================

        self.form_container = tk.Frame(
            self.right,
            bg="#FFFFFF"
        )

        # ==================================================
        # FORM CONTENT
        # ==================================================

        self.build_user_form()

    # ==================================================
    # USER FORM
    # ==================================================

    def build_user_form(self):

        self.form_container = tk.Frame(
            self.right,
            bg="#FFFFFF"
        )

        content = tk.Frame(
            self.form_container,
            bg="#FFFFFF"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # ==================================================
        # ACTION BUTTONS
        # FOOTER - DIKUNCI DI BAGIAN BAWAH
        # ==================================================

        action_frame = tk.Frame(
            content,
            bg="#FFFFFF",
            height=55
        )

        action_frame.pack(
            side="bottom",
            fill="x",
            pady=(10, 0)
        )

        action_frame.pack_propagate(
            False
        )

        self.save_button = tk.Button(
            action_frame,
            text="💾  SIMPAN",
            command=self.save_user,
            font=(
                "Arial",
                10,
                "bold"
            ),
            fg="white",
            bg="#2D7D5B",
            activebackground="#246A4C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        self.save_button.pack(
            side="left",
            padx=(0, 8)
        )

        self.delete_button = tk.Button(
            action_frame,
            text="🗑  HAPUS",
            command=self.delete_user,
            font=(
                "Arial",
                10,
                "bold"
            ),
            fg="white",
            bg="#B4232A",
            activebackground="#941D23",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            state="disabled"
        )

        self.delete_button.pack(
            side="left"
        )

        self.close_form_button = tk.Button(
            action_frame,
            text="TUTUP",
            command=self.hide_user_form,
            font=(
                "Arial",
                10,
                "bold"
            ),
            fg="white",
            bg="#607D8B",
            activebackground="#455A64",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        self.close_form_button.pack(
            side="right"
        )

        # ==================================================
        # TITLE
        # ==================================================

        self.form_title = tk.Label(
            content,
            text="DATA PENGGUNA",
            font=(
                "Arial",
                14,
                "bold"
            ),
            fg="#12372A",
            bg="#FFFFFF"
        )

        self.form_title.pack(
            anchor="w",
            pady=(0, 15)
        )

        # ==================================================
        # USERNAME
        # ==================================================

        self.create_form_label(
            content,
            "Username"
        )

        self.username_entry = tk.Entry(
            content,
            font=(
                "Arial",
                10
            )
        )

        self.username_entry.pack(
            fill="x",
            pady=(0, 10)
        )

        # ==================================================
        # PASSWORD
        # ==================================================

        self.create_form_label(
            content,
            "Password"
        )

        password_frame = tk.Frame(
            content,
            bg="#FFFFFF"
        )

        password_frame.pack(
            fill="x",
            pady=(0, 5)
        )

        self.password_entry = tk.Entry(
            password_frame,
            font=(
                "Arial",
                10
            ),
            show="●",
            textvariable=self.password_var
        )

        self.password_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.password_toggle_button = tk.Button(
            password_frame,
            text="◉  Lihat",
            command=self.toggle_password,
            font=(
                "Arial",
                9,
                "bold"
            ),
            fg="#12372A",
            bg="#E2E8F0",
            activebackground="#CBD5E1",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5
        )

        self.password_toggle_button.pack(
            side="left",
            padx=(8, 0)
        )

        self.password_hint = tk.Label(
            content,
            text=(
                "Untuk user baru password wajib diisi. "
                "Saat edit, kosongkan jika tidak ingin "
                "mengubah password."
            ),
            font=(
                "Arial",
                8
            ),
            fg="#64748B",
            bg="#FFFFFF",
            wraplength=600,
            justify="left"
        )

        self.password_hint.pack(
            anchor="w",
            pady=(0, 10)
        )

        # ==================================================
        # ROLE
        # ==================================================

        self.create_form_label(
            content,
            "Role"
        )

        self.role_frame = tk.Frame(
            content,
            bg="#FFFFFF"
        )

        self.role_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        self.role_menu = tk.OptionMenu(
            self.role_frame,
            self.role_var,
            "USER",
            "ADMIN",
            "SUPERADMIN",
            command=self.on_role_changed
        )

        self.role_menu.configure(
            font=(
                "Arial",
                10
            ),
            relief="flat",
            bg="#F8FAFC"
        )

        self.role_menu.pack(
            anchor="w"
        )

        # ==================================================
        # ACTIVE
        # ==================================================

        self.active_check = tk.Checkbutton(
            content,
            text="Akun aktif",
            variable=self.active_var,
            font=(
                "Arial",
                10,
                "bold"
            ),
            fg="#12372A",
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            selectcolor="#FFFFFF"
        )

        self.active_check.pack(
            anchor="w",
            pady=(5, 12)
        )

        # ==================================================
        # PERMISSION TITLE
        # ==================================================

        tk.Label(
            content,
            text="HAK AKSES ROLE",
            font=(
                "Arial",
                11,
                "bold"
            ),
            fg="#12372A",
            bg="#FFFFFF"
        ).pack(
            anchor="w",
            pady=(5, 8)
        )

        # ==================================================
        # PERMISSION CONTAINER
        # ==================================================

        permission_outer = tk.Frame(
            content,
            bg="#F8FAFC",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        permission_outer.pack(
            fill="both",
            expand=True
        )

        # ==================================================
        # PERMISSION CANVAS
        # ==================================================

        self.permission_canvas = tk.Canvas(
            permission_outer,
            bg="#F8FAFC",
            highlightthickness=0
        )

        permission_scrollbar = ttk.Scrollbar(
            permission_outer,
            orient="vertical",
            command=self.permission_canvas.yview
        )

        self.permission_canvas.configure(
            yscrollcommand=permission_scrollbar.set
        )

        permission_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.permission_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # PERMISSION FRAME
        # ==================================================

        self.permission_frame = tk.Frame(
            self.permission_canvas,
            bg="#F8FAFC"
        )

        self.permission_window = (
            self.permission_canvas.create_window(
                (0, 0),
                window=self.permission_frame,
                anchor="nw"
            )
        )

        self.permission_frame.bind(
            "<Configure>",
            self.on_permission_frame_configure
        )

        self.permission_canvas.bind(
            "<Configure>",
            self.on_permission_canvas_configure
        )
    # ==================================================
    # FORM LABEL
    # ==================================================

    def create_form_label(
        self,
        parent,
        text
    ):

        tk.Label(
            parent,
            text=text,
            font=(
                "Arial",
                9,
                "bold"
            ),
            fg="#12372A",
            bg="#FFFFFF"
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

    # ==================================================
    # PERMISSION SCROLL
    # ==================================================

    def on_permission_frame_configure(
        self,
        event=None
    ):

        self.permission_canvas.configure(
            scrollregion=(
                self.permission_canvas
                .bbox("all")
            )
        )

    def on_permission_canvas_configure(
        self,
        event
    ):

        self.permission_canvas.itemconfig(
            self.permission_window,
            width=event.width
        )

    # ==================================================
    # LOAD USERS
    # ==================================================

    def load_users(self):

        try:

            auth_service.load_users()

            self.user_list = list(
                auth_service.users
            )

            # Clear table.

            for item in self.user_table.get_children():

                self.user_table.delete(
                    item
                )

            # Populate table.

            for user in self.user_list:

                username = str(
                    user.get(
                        "username",
                        "-"
                    )
                )

                role = str(
                    user.get(
                        "role",
                        "USER"
                    )
                ).upper()

                active = bool(
                    user.get(
                        "active",
                        False
                    )
                )

                status = (
                    "AKTIF"
                    if active
                    else "NONAKTIF"
                )

                self.user_table.insert(
                    "",
                    "end",
                    values=(
                        username,
                        role,
                        status
                    )
                )

            self.edit_button.configure(
                state="disabled"
            )

            self.selected_username = None

        except Exception as error:

            messagebox.showerror(
                "Gagal Memuat User",
                str(error)
            )

    # ==================================================
    # USER SELECTED
    # ==================================================

    def on_user_selected(
        self,
        event=None
    ):

        selection = (
            self.user_table.selection()
        )

        if not selection:

            self.selected_username = None

            self.edit_button.configure(
                state="disabled"
            )

            return

        item_id = selection[0]

        values = self.user_table.item(
            item_id,
            "values"
        )

        if not values:

            return

        self.selected_username = (
            values[0]
        )

        self.edit_button.configure(
            state="normal"
        )

    # ==================================================
    # SHOW CREATE FORM
    # ==================================================

    def show_create_form(self):

        self.form_mode = "CREATE"

        self.selected_username = None

        self.empty_state.pack_forget()

        self.form_container.pack(
            fill="both",
            expand=True
        )

        self.form_title.configure(
            text="TAMBAH PENGGUNA"
        )

        self.username_entry.configure(
            state="normal"
        )

        self.username_entry.delete(
            0,
            "end"
        )

        self.password_var.set(
            ""
        )

        self.password_visible = False

        self.password_entry.configure(
            show="●"
        )

        self.password_toggle_button.configure(
            text="◉  Lihat"
        )

        self.role_var.set(
            "USER"
        )

        self.active_var.set(
            True
        )

        self.delete_button.configure(
            state="disabled"
        )

        self.save_button.configure(
            text="💾  SIMPAN USER"
        )

        self.active_check.configure(
            state="normal"
        )

        self.role_menu.configure(
            state="normal"
        )

        self.update_permission_display()

        self.username_entry.focus_set()

    # ==================================================
    # SHOW EDIT FORM
    # ==================================================

    def show_edit_form(self):

        selection = (
            self.user_table.selection()
        )

        if not selection:

            messagebox.showwarning(
                "Ubah Pengguna",
                (
                    "Pilih pengguna yang ingin "
                    "diubah terlebih dahulu."
                )
            )

            return

        item_id = selection[0]

        values = self.user_table.item(
            item_id,
            "values"
        )

        if not values:

            return

        username = str(
            values[0]
        )

        target = None

        for user in auth_service.users:

            if (
                user.get(
                    "username"
                )
                == username
            ):

                target = user
                break

        if target is None:

            messagebox.showerror(
                "Gagal",
                "Pengguna tidak ditemukan."
            )

            return

        self.form_mode = "EDIT"

        self.selected_username = username

        self.empty_state.pack_forget()

        self.form_container.pack(
            fill="both",
            expand=True
        )

        self.form_title.configure(
            text="UBAH DATA PENGGUNA"
        )

        self.username_entry.configure(
            state="normal"
        )

        self.username_entry.delete(
            0,
            "end"
        )

        self.username_entry.insert(
            0,
            username
        )

        self.username_entry.configure(
            state="disabled"
        )

        # Password lama TIDAK diambil.
        self.password_var.set(
            ""
        )

        self.password_visible = False

        self.password_entry.configure(
            show="●"
        )

        self.password_toggle_button.configure(
            text="◉  Lihat"
        )

        role = str(
            target.get(
                "role",
                "USER"
            )
        ).upper()

        self.role_var.set(
            role
        )

        self.active_var.set(
            bool(
                target.get(
                    "active",
                    False
                )
            )
        )

        self.save_button.configure(
            text="💾  SIMPAN PERUBAHAN"
        )

        self.delete_button.configure(
            state="normal"
        )

        current_username = (
            self.current_user.get(
                "username"
            )
        )

        if username == current_username:

            self.delete_button.configure(
                state="disabled"
            )

            self.active_check.configure(
                state="disabled"
            )

            self.role_menu.configure(
                state="disabled"
            )

        else:

            self.active_check.configure(
                state="normal"
            )

            self.role_menu.configure(
                state="normal"
            )

        self.update_permission_display()

    # ==================================================
    # HIDE FORM
    # ==================================================

    def hide_user_form(self):

        self.form_mode = None

        self.form_container.pack_forget()

        self.empty_state.pack(
            fill="both",
            expand=True
        )

        self.password_var.set(
            ""
        )

        self.password_visible = False

        self.password_entry.configure(
            show="●"
        )

        self.password_toggle_button.configure(
            text="◉  Lihat"
        )

    # ==================================================
    # PASSWORD TOGGLE
    # ==================================================

    def toggle_password(self):

        self.password_visible = (
            not self.password_visible
        )

        if self.password_visible:

            self.password_entry.configure(
                show=""
            )

            self.password_toggle_button.configure(
                text="●  Sembunyikan"
            )

        else:

            self.password_entry.configure(
                show="●"
            )

            self.password_toggle_button.configure(
                text="◉  Lihat"
            )

    # ==================================================
    # ROLE CHANGED
    # ==================================================

    def on_role_changed(
        self,
        value=None
    ):

        self.update_permission_display()

    # ==================================================
    # PERMISSION DISPLAY
    # ==================================================

    def update_permission_display(
        self,
        event=None
    ):

        role = str(
            self.role_var.get()
        ).upper()

        for widget in (
            self.permission_frame
            .winfo_children()
        ):

            widget.destroy()

        # ==================================================
        # ROLE LABEL
        # ==================================================

        tk.Label(
            self.permission_frame,
            text=f"ROLE: {role}",
            font=(
                "Consolas",
                9,
                "bold"
            ),
            fg="#12372A",
            bg="#F8FAFC"
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=10,
            pady=(10, 12)
        )

        try:

            permissions = sorted(
                permission_service.get_permissions(
                    role
                )
            )

        except Exception as error:

            permissions = []

            print(
                "[USER MANAGEMENT PERMISSION DISPLAY ERROR]",
                error
            )

        if not permissions:

            tk.Label(
                self.permission_frame,
                text="Tidak ada hak akses.",
                font=(
                    "Arial",
                    9
                ),
                fg="#64748B",
                bg="#F8FAFC"
            ).grid(
                row=1,
                column=0,
                columnspan=3,
                sticky="w",
                padx=10,
                pady=5
            )

            return

        # ==================================================
        # 3 COLUMN PERMISSION GRID
        # ==================================================

        for index, permission in enumerate(
            permissions
        ):

            row = (
                index // 3
            ) + 1

            column = (
                index % 3
            )

            tk.Label(
                self.permission_frame,
                text="☑  " + permission,
                font=(
                    "Consolas",
                    9
                ),
                fg="#334155",
                bg="#F8FAFC",
                anchor="w"
            ).grid(
                row=row,
                column=column,
                sticky="w",
                padx=10,
                pady=3
            )

        for column in range(3):

            self.permission_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.permission_canvas.update_idletasks()

        self.permission_canvas.configure(
            scrollregion=(
                self.permission_canvas
                .bbox("all")
            )
        )

    # ==================================================
    # SAVE USER
    # ==================================================

    def save_user(self):

        if self.form_mode not in (
            "CREATE",
            "EDIT"
        ):

            return

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_var
            .get()
        )

        role = (
            self.role_var
            .get()
            .strip()
            .upper()
        )

        active = (
            self.active_var
            .get()
        )

        # ==================================================
        # VALIDATION
        # ==================================================

        if not username:

            messagebox.showwarning(
                "Validasi",
                "Username wajib diisi."
            )

            return

        if not permission_service.is_valid_role(
            role
        ):

            messagebox.showwarning(
                "Validasi",
                "Role tidak valid."
            )

            return

        # ==================================================
        # CREATE
        # ==================================================

        if self.form_mode == "CREATE":

            if not password:

                messagebox.showwarning(
                    "Validasi",
                    (
                        "Password wajib diisi "
                        "untuk pengguna baru."
                    )
                )

                return

            if auth_service.username_exists(
                username
            ):

                messagebox.showwarning(
                    "Validasi",
                    "Username sudah digunakan."
                )

                return

            success = (
                auth_service.create_user(
                    username,
                    password,
                    role
                )
            )

            if not success:

                messagebox.showerror(
                    "Gagal",
                    "User gagal dibuat."
                )

                return

            # create_user membuat akun aktif.
            # Jika user diminta nonaktif,
            # ubah setelah dibuat.

            if not active:

                auth_service.load_users()

                for user in auth_service.users:

                    if (
                        user.get(
                            "username"
                        )
                        == username
                    ):

                        user["active"] = False

                        break

                auth_service.save_users()

            messagebox.showinfo(
                "Berhasil",
                "Pengguna berhasil dibuat."
            )

        # ==================================================
        # UPDATE
        # ==================================================

        else:

            target = None

            auth_service.load_users()

            for user in auth_service.users:

                if (
                    user.get(
                        "username"
                    )
                    == self.selected_username
                ):

                    target = user

                    break

            if target is None:

                messagebox.showerror(
                    "Gagal",
                    "Pengguna tidak ditemukan."
                )

                return

            current_username = (
                self.current_user.get(
                    "username"
                )
            )

            # ==================================================
            # PROTECT SELF
            # ==================================================

            if (
                target.get(
                    "username"
                )
                == current_username
            ):

                if not active:

                    messagebox.showwarning(
                        "Tidak Diizinkan",
                        (
                            "Akun yang sedang digunakan "
                            "tidak dapat dinonaktifkan."
                        )
                    )

                    return

                if role != "SUPERADMIN":

                    messagebox.showwarning(
                        "Tidak Diizinkan",
                        (
                            "Akun SUPERADMIN yang sedang "
                            "digunakan tidak boleh "
                            "diturunkan role-nya."
                        )
                    )

                    return

            # ==================================================
            # PROTECT LAST SUPERADMIN
            # ==================================================

            old_role = str(
                target.get(
                    "role",
                    "USER"
                )
            ).upper()

            if (
                old_role == "SUPERADMIN"
                and
                role != "SUPERADMIN"
            ):

                if self.count_superadmins() <= 1:

                    messagebox.showwarning(
                        "Tidak Diizinkan",
                        (
                            "Tidak dapat menurunkan role "
                            "SUPERADMIN terakhir."
                        )
                    )

                    return

            if (
                old_role == "SUPERADMIN"
                and
                not active
            ):

                if (
                    self.count_active_superadmins()
                    <= 1
                ):

                    messagebox.showwarning(
                        "Tidak Diizinkan",
                        (
                            "Tidak dapat menonaktifkan "
                            "SUPERADMIN aktif terakhir."
                        )
                    )

                    return

            # ==================================================
            # UPDATE
            # ==================================================

            target["role"] = role

            target["active"] = active

            if password:

                target["password_hash"] = (
                    auth_service.hash_password(
                        password
                    )
                )

            auth_service.save_users()

            messagebox.showinfo(
                "Berhasil",
                "Data pengguna berhasil diperbarui."
            )

        # ==================================================
        # REFRESH
        # ==================================================

        self.load_users()

        self.hide_user_form()

    # ==================================================
    # COUNT SUPERADMIN
    # ==================================================

    def count_superadmins(self):

        count = 0

        for user in auth_service.users:

            if (
                str(
                    user.get(
                        "role",
                        ""
                    )
                ).upper()
                == "SUPERADMIN"
            ):

                count += 1

        return count

    # ==================================================
    # COUNT ACTIVE SUPERADMIN
    # ==================================================

    def count_active_superadmins(self):

        count = 0

        for user in auth_service.users:

            if (

                str(
                    user.get(
                        "role",
                        ""
                    )
                ).upper()
                == "SUPERADMIN"

                and

                bool(
                    user.get(
                        "active",
                        False
                    )
                )

            ):

                count += 1

        return count

    # ==================================================
    # DELETE USER
    # ==================================================

    def delete_user(self):

        if self.form_mode != "EDIT":

            return

        if not self.selected_username:

            return

        username = (
            self.selected_username
        )

        current_username = (
            self.current_user.get(
                "username"
            )
        )

        # ==================================================
        # PROTECT SELF
        # ==================================================

        if username == current_username:

            messagebox.showwarning(
                "Tidak Diizinkan",
                (
                    "Akun yang sedang digunakan "
                    "tidak dapat dihapus."
                )
            )

            return

        # ==================================================
        # FIND TARGET
        # ==================================================

        target = None

        for user in auth_service.users:

            if (
                user.get(
                    "username"
                )
                == username
            ):

                target = user

                break

        if target is None:

            messagebox.showerror(
                "Gagal",
                "Pengguna tidak ditemukan."
            )

            return

        role = str(
            target.get(
                "role",
                "USER"
            )
        ).upper()

        # ==================================================
        # PROTECT LAST SUPERADMIN
        # ==================================================

        if (
            role == "SUPERADMIN"
            and
            self.count_superadmins() <= 1
        ):

            messagebox.showwarning(
                "Tidak Diizinkan",
                (
                    "SUPERADMIN terakhir tidak "
                    "dapat dihapus."
                )
            )

            return

        # ==================================================
        # CONFIRM
        # ==================================================

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            (
                "Apakah Anda yakin ingin "
                f"menghapus pengguna '{username}'?"
            )
        )

        if not confirm:

            return

        # ==================================================
        # DELETE
        # ==================================================

        auth_service.users = [
            user
            for user in auth_service.users
            if user.get(
                "username"
            ) != username
        ]

        auth_service.save_users()

        messagebox.showinfo(
            "Berhasil",
            "Pengguna berhasil dihapus."
        )

        self.load_users()

        self.hide_user_form()

    # ==================================================
    # CLOSE WINDOW
    # ==================================================

    def close(self):

        try:

            self.window.grab_release()

        except Exception:

            pass

        self.window.destroy()

    # ==================================================
    # RUN
    # ==================================================

    def run(self):

        if not self.check_access():

            messagebox.showerror(
                "Akses Ditolak",
                (
                    "Anda tidak memiliki hak "
                    "untuk membuka Manajemen Pengguna."
                ),
                parent=self.parent
            )

            self.window.destroy()

            return

        self.window.grab_set()

        self.window.focus_force()