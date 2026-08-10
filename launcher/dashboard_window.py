import os
import tkinter as tk

from tkinter import messagebox

from datetime import datetime

from PIL import Image, ImageTk

from services.branding_service import branding_service
from services.permission_service import permission_service
from services.system_controller import system_controller
from windows.report_window import ReportWindow
from windows.control_center_window import ControlCenterWindow


class DashboardWindow:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(
        self,
        current_user,
        on_logout=None,
        on_close=None
    ):

        self.current_user = current_user

        self.on_logout_callback = on_logout

        self.on_close_callback = on_close

        # ==================================================
        # BRANDING
        # ==================================================

        self.branding = (
            branding_service
            .get_branding()
        )

        self.system_name = (
            self.branding.get(
                "system_name",
                "SATRIA MAS BINANGUN"
            )
        )

        self.institution_name = (
            self.branding.get(
                "institution_name",
                ""
            )
        )

        self.header_title = (
            self.branding.get(
                "header_title",
                ""
            )
        )

        self.header_description = (
            self.branding.get(
                "header_description",
                ""
            )
        )

        self.footer_text = (
            self.branding.get(
                "footer_text",
                ""
            )
        )

        self.logo_path = (
            self.branding.get(
                "logo",
                "assets/logo.png"
            )
        )


        # ==================================================
        # ROOT
        # ==================================================

        self.root = tk.Toplevel()

        self.root.title(
            f"{self.system_name} - Dashboard"
        )

        self.root.geometry(
            "1200x800"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.resizable(
            True,
            True
        )

        # ==================================================
        # THEME
        # ==================================================

        self.theme = (
            branding_service
                .get_theme()

        )

        self.primary_color = (
            self.theme.get(
                "primary_color"
            )
        )

        self.accent_color = (
            self.theme.get(
                "accent_color",
                "#2D6A4F"
            )
        )

        self.background_color = "#F3F5F6"

        self.card_color = "#FFFFFF"

        self.text_color = "#12372A"

        self.muted_color = "#64748B"

        self.dark_color = "#17212B"

        # ==================================================
        # STATUS
        # ==================================================

        self.backend_status = "OFFLINE"

        self.bot_process_status = "OFFLINE"

        self.whatsapp_status = "OFFLINE"

        self.internet_status = "UNKNOWN"

        self.database_status = "NOT_READY"

        self.overall_status = "OFFLINE"

        # ==================================================
        # CONTROL FLAGS
        # ==================================================

        self.is_closing = False

        self.is_logging_out = False

        self.operation_in_progress = False

        self.active_operation = None

        # ==================================================
        # BUTTON REGISTRY
        # ==================================================

        self.control_buttons = []

        self.utility_buttons = []

        # ==================================================
        # LOG STORAGE
        # ==================================================

        self.system_logs = []

        self.log_window = None

       # ==================================================
       # SYSTEM CONTROLLER LOG CALLBACK
       # ==================================================
        system_controller.set_log_callback(
            self.receive_controller_log
        )

        # ==================================================
        # WINDOW CLOSE PROTOCOL
        # ==================================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.handle_close
        )

        # ==================================================
        # BUILD UI
        # ==================================================

        self.build_ui()

        # ==================================================
        # INITIAL STATUS
        # ==================================================

        self.refresh_status()

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
                "[PERMISSION ERROR]",
                error
            )

            return False

    # ==================================================
    # BUILD UI
    # ==================================================

    def build_ui(self):

        self.main_frame = tk.Frame(
            self.root,
            bg=self.background_color
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        self.build_header()

        self.canvas = tk.Canvas(
            self.main_frame,
            bg=self.background_color,
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar = tk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
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

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.build_system_overview()

        self.build_control_section()

        self.build_utilities_section()

        self.build_activity_section()

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

    def on_mousewheel(
        self,
        event
    ):

        self.canvas.yview_scroll(
            int(
                -1 *
                (
                    event.delta /
                    120
                )
            ),
            "units"
        )

    # ==================================================
    # HEADER
    # ==================================================

    def build_header(self):

        self.header_frame = tk.Frame(
            self.main_frame,
            bg=self.primary_color,
            height=160
        )

        self.header_frame.pack(
            fill="x"
        )

        self.header_frame.pack_propagate(
            False
        )

        header_content = tk.Frame(
            self.header_frame,
            bg=self.primary_color
        )

        header_content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=18
        )

        self.logo_photo = None

        try:

            logo_image = Image.open(
                self.logo_path
            )

            logo_image.thumbnail(
                (150, 150)
            )

            self.logo_photo = ImageTk.PhotoImage(
                logo_image
            )

            logo_label = tk.Label(
                header_content,
                image=self.logo_photo,
                bg=self.primary_color
            )

            logo_label.pack(
                side="left",
                padx=(0, 18)
            )

        except Exception as error:

            print(
                "[BRANDING] Logo gagal dimuat:",
                error
            )

        text_frame = tk.Frame(
            header_content,
            bg=self.primary_color
        )

        text_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            text_frame,
            text=self.system_name,
            font=("Arial", 25, "bold"),
            fg="white",
            bg=self.primary_color,
            anchor="w"
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_frame,
            text=self.institution_name,
            font=("Arial", 10, "bold"),
            fg="#D1FAE5",
            bg=self.primary_color,
            anchor="w"
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_frame,
            text=self.header_title,
            font=("Arial", 13),
            fg="#E5E7EB",
            bg=self.primary_color,
            anchor="w"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        if self.header_description:

            tk.Label(
                text_frame,
                text=self.header_description,
                font=("Arial", 9),
                fg="#D1D5DB",
                bg=self.primary_color,
                anchor="w",
                justify="left",
                wraplength=600
            ).pack(
                anchor="w",
                pady=(4, 0)
            )

        right_frame = tk.Frame(
            header_content,
            bg=self.primary_color
        )

        right_frame.pack(
            side="right",
            anchor="ne"
        )

        role = (
            self.current_user.get(
                "role",
                "USER"
            )
        )

        username = (
            self.current_user.get(
                "username",
                "-"
            )
        )

        tk.Label(
            right_frame,
            text=username,
            font=("Arial", 11, "bold"),
            fg="white",
            bg=self.primary_color
        ).pack(
            anchor="e"
        )

        tk.Label(
            right_frame,
            text=role,
            font=("Arial", 9, "bold"),
            fg="#D1FAE5",
            bg=self.primary_color
        ).pack(
            anchor="e"
        )

        tk.Button(
            right_frame,
            text="⎋  LOGOUT",
            command=self.logout,
            font=("Arial", 9, "bold"),
            fg="white",
            bg="#8B1E2D",
            activebackground="#A52A3A",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5
        ).pack(
            anchor="e",
            pady=(10, 0)
        )

    # ==================================================
    # SYSTEM OVERVIEW
    # ==================================================

    def build_system_overview(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        tk.Label(
            section,
            text="SYSTEM OVERVIEW",
            font=("Arial", 17, "bold"),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        self.overall_status_frame = tk.Frame(
            section,
            bg=self.card_color,
            highlightbackground="#CBD5E1",
            highlightthickness=1,
            height=90
        )

        self.overall_status_frame.pack(
            fill="x",
            pady=(0, 12)
        )

        self.overall_status_frame.pack_propagate(
            False
        )

        self.overall_status_label = tk.Label(
            self.overall_status_frame,
            text="● OFFLINE",
            font=("Arial", 20, "bold"),
            fg="#C62832",
            bg=self.card_color
        )

        self.overall_status_label.pack(
            pady=(14, 0)
        )

        self.overall_description_label = tk.Label(
            self.overall_status_frame,
            text="System status sedang diperiksa.",
            font=("Arial", 9),
            fg=self.muted_color,
            bg=self.card_color
        )

        self.overall_description_label.pack()

        self.status_cards_frame = tk.Frame(
            section,
            bg=self.background_color
        )

        self.status_cards_frame.pack(
            fill="x"
        )

        for column in range(5):

            self.status_cards_frame.columnconfigure(
                column,
                weight=1
            )

        self.status_card_widgets = {}

        self.create_status_card(
            0,
            "BACKEND",
            self.backend_status,
            "Port 5000"
        )

        self.create_status_card(
            1,
            "BOT PROCESS",
            self.bot_process_status,
            "Node.js"
        )

        self.create_status_card(
            2,
            "WHATSAPP",
            self.whatsapp_status,
            "Connection"
        )

        self.create_status_card(
            3,
            "INTERNET",
            self.internet_status,
            "Network"
        )

        self.create_status_card(
            4,
            "DATABASE",
            self.database_status,
            "Knowledge"
        )

    # ==================================================
    # STATUS CARD
    # ==================================================

    def create_status_card(
        self,
        column,
        title,
        status,
        subtitle
    ):

        card = tk.Frame(
            self.status_cards_frame,
            bg=self.card_color,
            highlightbackground="#CBD5E1",
            highlightthickness=1,
            height=115
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=4
        )

        card.grid_propagate(
            False
        )

        self.status_card_widgets[title] = {
            "card": card,
            "subtitle": subtitle
        }

        self.render_status_card(
            title,
            status
        )

    def render_status_card(
        self,
        title,
        status
    ):

        card_data = (
            self.status_card_widgets.get(
                title
            )
        )

        if not card_data:

            return

        card = card_data["card"]

        subtitle = card_data["subtitle"]

        for widget in card.winfo_children():

            widget.destroy()

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            fg="#5B7EA2",
            bg=self.card_color
        ).pack(
            pady=(16, 2)
        )

        status_color = (
            self.get_status_color(
                status
            )
        )

        status_frame = tk.Frame(
            card,
            bg=self.card_color
        )

        status_frame.pack()

        tk.Label(
            status_frame,
            text="●",
            font=("Arial", 16),
            fg=status_color,
            bg=self.card_color
        ).pack(
            side="left",
            padx=(0, 5)
        )

        tk.Label(
            status_frame,
            text=status,
            font=("Arial", 14, "bold"),
            fg=status_color,
            bg=self.card_color
        ).pack(
            side="left"
        )

        tk.Label(
            card,
            text=subtitle,
            font=("Arial", 8),
            fg=self.muted_color,
            bg=self.card_color
        ).pack(
            pady=(3, 0)
        )

    # ==================================================
    # STATUS COLOR
    # ==================================================

    def get_status_color(
        self,
        status
    ):

        status = str(
            status
        ).upper()

        if status in (
            "ONLINE",
            "CONNECTED",
            "RUNNING",
            "READY",
            "OPERATIONAL"
        ):

            return "#267A5A"

        if status in (
            "STARTING",
            "STOPPING",
            "RESTARTING",
            "CHECKING",
            "DEGRADED",
            "INTERNET_OFFLINE",
            "UNKNOWN"
        ):

            return "#C8741A"

        return "#C62832"

    # ==================================================
    # CONTROL SECTION
    # ==================================================

    def build_control_section(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=30,
            pady=(24, 10)
        )

        tk.Label(
            section,
            text="SYSTEM CONTROL",
            font=("Arial", 17, "bold"),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        buttons = tk.Frame(
            section,
            bg=self.background_color
        )

        buttons.pack(
            fill="x"
        )

        for column in range(4):

            buttons.columnconfigure(
                column,
                weight=1
            )

        self.create_control_button(
            buttons,
            0,
            "START_SYSTEM",
            "▶  START SYSTEM",
            self.start_system,
            "#2D7D5B"
        )

        self.create_control_button(
            buttons,
            1,
            "STOP_SYSTEM",
            "■  STOP SYSTEM",
            self.stop_system,
            "#B4232A"
        )

        self.create_control_button(
            buttons,
            2,
            "RESTART_SYSTEM",
            "↻  RESTART SYSTEM",
            self.restart_system,
            "#C8741A"
        )

        self.create_control_button(
            buttons,
            3,
            "CHECK_SYSTEM",
            "✓  CHECK SYSTEM",
            self.check_system,
            "#4F89AD"
        )

    # ==================================================
    # CONTROL BUTTON
    # ==================================================

    def create_control_button(
        self,
        parent,
        column,
        key,
        text,
        command,
        color
    ):

        allowed = self.has_permission(
            key
        )

        if allowed:

            button = tk.Button(
                parent,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                fg="white",
                bg=color,
                activebackground=color,
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                height=2
            )

            self.control_buttons.append(
                {
                    "key": key,
                    "button": button
                }
            )

        else:

            button = tk.Button(
                parent,
                text=text,
                state="disabled",
                font=("Arial", 10, "bold"),
                fg="#6B7280",
                bg="#D1D5DB",
                relief="flat",
                height=2
            )

        button.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

    # ==================================================
    # UTILITIES
    # ==================================================

    def build_utilities_section(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=30,
            pady=(24, 10)
        )

        tk.Label(
            section,
            text="QUICK ACTIONS",
            font=("Arial", 17, "bold"),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        buttons = tk.Frame(
            section,
            bg=self.background_color
        )

        buttons.pack(
            fill="x"
        )

        for column in range(4):

            buttons.columnconfigure(
                column,
                weight=1
            )

        self.create_utility_button(
            buttons,
            0,
            "📊  LAPORAN",
            "VIEW_REPORT",
            self.open_report
        )

        self.create_utility_button(
            buttons,
            1,
            "⚙️  PUSAT KENDALI",
            "SYSTEM_CONFIGURATION",
            self.open_control_center
        )

        self.create_utility_button(
            buttons,
            2,
            "📜  VIEW LOG",
            "VIEW_LOG",
            self.view_log
        )

        self.create_utility_button(
            buttons,
            3,
            "🧹  CLEAN CACHE",
            "CLEAN_CACHE",
            self.clean_cache
        )

    # ==================================================
    # UTILITY BUTTON
    # ==================================================

    def create_utility_button(
        self,
        parent,
        column,
        text,
        permission,
        command
    ):

        allowed = self.has_permission(
            permission
        )

        if allowed:

            button = tk.Button(
                parent,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                fg="white",
                bg="#607D8B",
                activebackground="#455A64",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                height=2
            )

            self.utility_buttons.append(
                {
                    "button": button,
                    "permission": permission
                }
            )

        else:

            button = tk.Button(
                parent,
                text=text,
                state="disabled",
                font=("Arial", 10, "bold"),
                fg="#6B7280",
                bg="#D1D5DB",
                relief="flat",
                height=2
            )

        button.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

    # ==================================================
    # ACTIVITY
    # ==================================================

    def build_activity_section(self):

        section = tk.Frame(
            self.scrollable_frame,
            bg=self.background_color
        )

        section.pack(
            fill="x",
            padx=30,
            pady=(24, 10)
        )

        header = tk.Frame(
            section,
            bg=self.background_color
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="RECENT ACTIVITY",
            font=("Arial", 17, "bold"),
            fg=self.text_color,
            bg=self.background_color
        ).pack(
            side="left"
        )

        if self.has_permission(
            "VIEW_LOG"
        ):

            tk.Button(
                header,
                text="VIEW ALL LOG",
                command=self.view_log,
                font=("Arial", 9, "bold"),
                fg=self.accent_color,
                bg=self.background_color,
                relief="flat",
                cursor="hand2"
            ).pack(
                side="right"
            )

        self.activity_text = tk.Text(
            section,
            height=7,
            bg=self.dark_color,
            fg="#E5E7EB",
            font=("Consolas", 9),
            relief="flat",
            padx=10,
            pady=10,
            state="disabled"
        )

        self.activity_text.pack(
            fill="x",
            pady=(10, 0)
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
            padx=30,
            pady=(25, 25)
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
            text=self.footer_text,
            font=("Arial", 9),
            fg=self.muted_color,
            bg=self.background_color
        ).pack()

    # ==================================================
    # LOG
    # ==================================================

    def receive_controller_log(
        self,
        message
    ):

        if self.is_closing:

            return

        self.system_logs.append(
            message
        )

        self.refresh_activity()

        if (

            self.log_window

            and

            self.log_window.winfo_exists()

        ):

            self.refresh_log_window()

    def write_log(
        self,
        message
    ):

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        line = (
            f"[{timestamp}] {message}"
        )

        self.system_logs.append(
            line
        )

        self.refresh_activity()

        if (
            self.log_window
            and
            self.log_window.winfo_exists()
        ):

            self.refresh_log_window()

    def refresh_activity(self):

        if not hasattr(
            self,
            "activity_text"
        ):

            return

        self.activity_text.configure(
            state="normal"
        )

        self.activity_text.delete(
            "1.0",
            "end"
        )

        recent_logs = (
            self.system_logs[-8:]
        )

        for line in recent_logs:

            self.activity_text.insert(
                "end",
                line + "\n"
            )

        self.activity_text.see(
            "end"
        )

        self.activity_text.configure(
            state="disabled"
        )

    # ==================================================
    # OPERATION LOCK
    # ==================================================

    def acquire_operation_lock(
        self,
        operation_name
    ):

        if self.operation_in_progress:

            self.write_log(
                "Perintah "
                + operation_name
                + " ditolak. Operasi "
                + str(
                    self.active_operation
                )
                + " masih berjalan."
            )

            return False

        self.operation_in_progress = True

        self.active_operation = (
            operation_name
        )

        self.set_operation_lock(
            True
        )

        self.write_log(
            operation_name
            + " LOCKED."
        )

        return True


    def release_operation_lock(
        self
    ):

        self.operation_in_progress = False

        self.active_operation = None

        self.set_operation_lock(
            False
        )

    def set_operation_lock(
        self,
        locked
    ):

        self.operation_in_progress = locked

        if locked:

            for button_data in self.control_buttons:

                button_data["button"].configure(
                    state="disabled"
                )

            for button_data in self.utility_buttons:
                button_data["button"].configure(
                    state="disabled"
                )


        else:

                          self.update_control_buttons()

                          for button_data in self.utility_buttons:

                              button = (
                                  button_data["button"]
                              )

                              permission = (
                                  button_data["permission"]
                              )

                              if self.has_permission(
                                  permission
                              ):

                                  button.configure(
                                      state="normal"
                                  )

                              else:

                                  button.configure(
                                      state="disabled"
                                  )
    # ==================================================
    # REFRESH STATUS
    # ==================================================

    def refresh_status(self):

        if self.is_closing:

            return

        try:

            status = (
                system_controller
                .check_system()
            )

            # ==========================================
            # BACKEND
            # ==========================================

            if (
                status.get(
                    "backend_port",
                    False
                )
                and
                status.get(
                    "backend_ready",
                    False
                )
            ):

                self.backend_status = "ONLINE"

            else:

                self.backend_status = "OFFLINE"

            # ==========================================
            # BOT
            # ==========================================

            if status.get(
                "bot_process",
                False
            ):

                self.bot_process_status = "ONLINE"

            else:

                self.bot_process_status = "OFFLINE"

            # ==========================================
            # INTERNET
            # ==========================================

            if status.get(
                "internet_available",
                False
            ):

                self.internet_status = "ONLINE"

            else:

                self.internet_status = "OFFLINE"

            # ==========================================
            # WHATSAPP
            # ==========================================

            if status.get(
                "bot_process",
                False
            ):

                self.whatsapp_status = "RUNNING"

            else:

                self.whatsapp_status = "OFFLINE"

            # ==========================================
            # DATABASE
            # ==========================================

            if status.get(
                "backend_ready",
                False
            ):

                self.database_status = "READY"

            else:

                self.database_status = "NOT_READY"

            # ==========================================
            # OVERALL
            # ==========================================

            self.update_status_cards()

            self.update_overall_status()

            self.update_control_buttons()

        except Exception as error:

            self.write_log(
                "Gagal memperbarui status: "
                + str(error)
            )

        if not self.is_closing:

            self.root.after(
                5000,
                self.refresh_status
            )

    # ==================================================
    # UPDATE STATUS CARDS
    # ==================================================

    def update_status_cards(self):

        status_map = {

            "BACKEND":
                self.backend_status,

            "BOT PROCESS":
                self.bot_process_status,

            "WHATSAPP":
                self.whatsapp_status,

            "INTERNET":
                self.internet_status,

            "DATABASE":
                self.database_status

        }

        for title, status in status_map.items():

            self.render_status_card(
                title,
                status
            )

    # ==================================================
    # OVERALL STATUS
    # ==================================================

    def update_overall_status(self):

        backend = (
            self.backend_status.upper()
        )

        bot = (
            self.bot_process_status.upper()
        )

        internet = (
            self.internet_status.upper()
        )

        whatsapp = (
            self.whatsapp_status.upper()
        )

        database = (
            self.database_status.upper()
        )

        # ==========================================
        # ONLINE
        # ==========================================

        if (
            backend == "ONLINE"
            and
            bot == "ONLINE"
            and
            whatsapp == "RUNNING"
            and
            internet == "ONLINE"
            and
            database == "READY"
        ):

            overall = "ONLINE"

            description = (
                "SATRIA MAS SUDAH BEKERJA UNTUK ANDA"
            )

        # ==========================================
        # INTERNET OFFLINE
        # ==========================================

        elif (
            backend == "ONLINE"
            and
            bot == "ONLINE"
            and
            internet == "OFFLINE"
        ):

            overall = "INTERNET_OFFLINE"

            description = (
                "Backend dan bot aktif, tetapi koneksi internet tidak tersedia."
            )

        # ==========================================
        # BACKEND ONLY
        # ==========================================

        elif (
            backend == "ONLINE"
            and
            bot != "ONLINE"
        ):

            overall = "BACKEND ONLY"

            description = (
                "Backend aktif, tetapi bot process belum berjalan."
            )

        # ==========================================
        # DEGRADED
        # ==========================================

        elif (
            backend == "ONLINE"
            and
            bot == "ONLINE"
            and
            whatsapp != "RUNNING"
        ):

            overall = "DEGRADED"

            description = (
                "Backend dan bot aktif, tetapi koneksi WhatsApp bermasalah."
            )

        # ==========================================
        # OFFLINE
        # ==========================================

        else:

            overall = "OFFLINE"

            description = (
                "Satu atau lebih komponen utama tidak siap."
            )

        self.overall_status = overall

        self.overall_status_label.configure(
            text="● " + overall,
            fg=self.get_status_color(
                overall
            )
        )

        self.overall_description_label.configure(
            text=description
        )

    # ==================================================
    # UPDATE CONTROL BUTTONS
    # ==================================================

    def update_control_buttons(self):

        if self.operation_in_progress:

            for button_data in self.control_buttons:

                button_data["button"].configure(
                    state="disabled"
                )

            return

        system = (
            str(
                self.overall_status
            )
            .upper()
        )

        start_state = "disabled"

        stop_state = "disabled"

        restart_state = "disabled"

        check_state = "normal"

        # ==========================================
        # OFFLINE
        # ==========================================

        if system == "OFFLINE":

            start_state = "normal"

            stop_state = "disabled"

            restart_state = "disabled"

        # ==========================================
        # BACKEND ONLY
        # ==========================================

        elif system == "BACKEND ONLY":

            start_state = "normal"

            stop_state = "normal"

            restart_state = "normal"

        # ==========================================
        # ONLINE
        # ==========================================

        elif system == "ONLINE":

            start_state = "disabled"

            stop_state = "normal"

            restart_state = "normal"

        # ==========================================
        # INTERNET OFFLINE
        # ==========================================

        elif system == "INTERNET_OFFLINE":

            start_state = "disabled"

            stop_state = "normal"

            restart_state = "normal"

        # ==========================================
        # DEGRADED
        # ==========================================

        elif system == "DEGRADED":

            start_state = "normal"

            stop_state = "normal"

            restart_state = "normal"

        # ==========================================
        # TRANSITION
        # ==========================================

        elif system in (
            "STARTING",
            "STOPPING",
            "RESTARTING",
            "CHECKING"
        ):

            start_state = "disabled"

            stop_state = "disabled"

            restart_state = "disabled"

            check_state = "disabled"

        button_map = {

            "START_SYSTEM":
                start_state,

            "STOP_SYSTEM":
                stop_state,

            "RESTART_SYSTEM":
                restart_state,

            "CHECK_SYSTEM":
                check_state

        }

        for button_data in self.control_buttons:

            key = (
                button_data.get(
                    "key"
                )
            )

            button = (
                button_data.get(
                    "button"
                )
            )

            if key in button_map:

                button.configure(
                    state=button_map[key]
                )

    # ==================================================
    # START SYSTEM
    # ==================================================

    def start_system(self):

        if not self.acquire_operation_lock(
            "START_SYSTEM"

        ):

            return



        self.write_log(
            "START SYSTEM dimulai."
        )

        try:

            success = (
                system_controller
                .start_system()
            )

            if success:

                self.write_log(
                    "START SYSTEM BERHASIL."
                )

                messagebox.showinfo(
                    self.system_name,
                    "Sistem berhasil dijalankan."
                )

            else:

                self.write_log(
                    "START SYSTEM GAGAL."
                )

                messagebox.showerror(
                    self.system_name,
                    "Sistem gagal dijalankan."
                )

        except Exception as error:

            self.write_log(
                "Error START SYSTEM: "
                + str(error)
            )

            messagebox.showerror(
                self.system_name,
                str(error)
            )

        finally:

            self.release_operation_lock()

            self.refresh_status()

    # ==================================================
    # STOP SYSTEM
    # ==================================================

    def stop_system(self):

        if self.operation_in_progress:

            return

        confirm = messagebox.askyesno(
            "Konfirmasi STOP SYSTEM",
            "Apakah Anda yakin ingin menghentikan seluruh sistem?"
        )

        if not confirm:

            return

        if not self.acquire_operation_lock(
            "STOP_SYSTEM"
        ):

            return

        self.write_log(
            "STOP SYSTEM dimulai."
        )

        try:

            success = (
                system_controller
                .stop_system()
            )

            if success:

                self.write_log(
                    "STOP SYSTEM BERHASIL."
                )

                messagebox.showinfo(
                    self.system_name,
                    "Sistem berhasil dihentikan."
                )

            else:

                self.write_log(
                    "STOP SYSTEM GAGAL."
                )

                messagebox.showerror(
                    self.system_name,
                    "Sistem gagal dihentikan."
                )

        except Exception as error:

            self.write_log(
                "Error STOP SYSTEM: "
                + str(error)
            )

            messagebox.showerror(
                self.system_name,
                str(error)
            )

        finally:

            self.release_operation_lock()

            self.refresh_status()

    # ==================================================
    # RESTART SYSTEM
    # ==================================================

    def restart_system(self):

        if self.operation_in_progress:

            return

        confirm = messagebox.askyesno(
            "Konfirmasi RESTART SYSTEM",
            "Sistem akan dihentikan kemudian dijalankan kembali. Lanjutkan?"
        )

        if not confirm:

            return

        if not self.acquire_operation_lock(
            "RESTART_SYSTEM"
        ):

            return

        self.write_log(
            "RESTART SYSTEM dimulai."
        )

        try:

            success = (
                system_controller
                .restart_bot()
            )

            if success:

                self.write_log(
                    "RESTART SYSTEM BERHASIL."
                )

                messagebox.showinfo(
                    self.system_name,
                    "Sistem berhasil dijalankan kembali."
                )

            else:

                self.write_log(
                    "RESTART SYSTEM GAGAL."
                )

                messagebox.showerror(
                    self.system_name,
                    "Sistem gagal dijalankan kembali."
                )

        except Exception as error:

            self.write_log(
                "Error RESTART SYSTEM: "
                + str(error)
            )

            messagebox.showerror(
                self.system_name,
                str(error)
            )

        finally:

            self.release_operation_lock()

            self.refresh_status()

    # ==================================================
    # CHECK SYSTEM
    # ==================================================

    def check_system(self):

        if not self.acquire_operation_lock(

            "CHECK_SYSTEM"

        ): 

            return

        self.write_log(

            "CHECK SYSTEM dijalankan."

        )

        try:

            result = (

                system_controller

                .check_system()

            )

            if not result:

                self.write_log(

                    "CHECK SYSTEM gagal memperoleh hasil."

                )

                messagebox.showerror(

                    self.system_name,

                    "CHECK SYSTEM gagal memperoleh status sistem."

                )

                return

            system_status = str(

                result.get(

                    "system",

                    "OFFLINE"

                )

            ).upper()

            self.write_log(

                "CHECK SYSTEM selesai. Status: "

                + system_status

            )

            # ==================================================
            # STATUS BERHASIL DIPERIKSA
            # ==================================================

            if system_status == "ONLINE":

                messagebox.showinfo(

                    self.system_name,

                    "CHECK SYSTEM selesai.\n\n"

                    "Seluruh komponen utama siap digunakan.\n\n"

                    "Status: ONLINE"

                )

            # ==================================================
            # BACKEND AKTIF, BOT BELUM AKTIF
            # ==================================================

            elif system_status == "STANDBY":

                messagebox.showwarning(

                    self.system_name,

                    "CHECK SYSTEM selesai.\n\n"

                    "Backend aktif, tetapi Bot belum berjalan.\n\n"

                    "Status: STANDBY"

                )

            # ==================================================
            # SISTEM OFFLINE
            # ==================================================

            else:

                messagebox.showwarning(

                    self.system_name,

                    "CHECK SYSTEM selesai.\n\n"

                    "Terdapat komponen sistem yang belum aktif.\n\n"

                    "Status: "

                    + system_status

                )

        except Exception as error:

            self.write_log(

                "Error CHECK SYSTEM: "

                + str(error)

            )

            messagebox.showerror(

                self.system_name,

                str(error)

            )

        finally:

            self.release_operation_lock()

            self.refresh_status()

       #=======================================
       # LAPORAN
    #=======================================

    def open_report(self):

        if self.operation_in_progress:

            return

        self.write_log(

            "LAPORAN dibuka."

        )

        try:

            ReportWindow(

                self.root,

                current_user=self.current_user

            )

        except Exception as error:

            self.write_log(

                "Gagal membuka laporan: "

                +

                str(error)

            )

            messagebox.showerror(

                self.system_name,

                "Gagal membuka modul laporan.\n\n"

                +

                str(error)

            )

          # =========================================
          # PUSAT KENDALI
          # =========================================

    def open_control_center(self):

        if self.operation_in_progress:

            return

        self.write_log(
            "PUSAT KENDALI dibuka."
        )

        try:

            ControlCenterWindow(
                self.root,
                current_user=self.current_user
            )

        except Exception as error:

            self.write_log(
                "Gagal membuka Pusat Kendali: "
                + str(error)
            )

            messagebox.showerror(
                self.system_name,
                "Gagal membuka Pusat Kendali.\n\n"
                + str(error)
            )

    # ==================================================
    # CLEAN CACHE
    # ==================================================

    def clean_cache(self):

        if self.operation_in_progress:

            return

        self.set_operation_lock(
            True
        )

        self.write_log(
            "CLEAN CACHE dimulai."
        )

        try:

            success = (
                system_controller
                .clean_cache()
            )

            if success:

                self.write_log(
                    "CLEAN CACHE BERHASIL."
                )

                messagebox.showinfo(
                    self.system_name,
                    "Cache sementara berhasil dibersihkan."
                )

            else:

                self.write_log(
                    "CLEAN CACHE GAGAL."
                )

                messagebox.showerror(
                    self.system_name,
                    "CLEAN CACHE gagal dijalankan."
                )

        except Exception as error:

            self.write_log(
                "Error CLEAN CACHE: "
                + str(error)
            )

            messagebox.showerror(
                self.system_name,
                str(error)
            )

        finally:

            self.set_operation_lock(
                False
            )

            self.refresh_status()
    # ==================================================
    # SYSTEM DIAGNOSTIC
    # ==================================================

    def system_diagnostic(self):

        if self.operation_in_progress:

            return

        self.write_log(
            "SYSTEM DIAGNOSTIC dijalankan."
        )

        try:

            result = (
                system_controller
                .check_system()
            )

            diagnostic_window = tk.Toplevel(
                self.root
            )

            diagnostic_window.title(
                "SYSTEM DIAGNOSTIC"
            )

            diagnostic_window.geometry(
                "600x500"
            )

            diagnostic_window.configure(
                bg=self.background_color
            )

            text = tk.Text(
                diagnostic_window,
                bg=self.dark_color,
                fg="#E5E7EB",
                font=("Consolas", 10),
                relief="flat",
                padx=12,
                pady=12
            )

            text.pack(
                fill="both",
                expand=True,
                padx=15,
                pady=15
            )

            for key, value in result.items():

                text.insert(
                    "end",
                    f"{key:<25}: {value}\n"
                )

            text.configure(
                state="disabled"
            )

        except Exception as error:

            self.write_log(
                "Error SYSTEM DIAGNOSTIC: "
                + str(error)
            )

            messagebox.showerror(
                self.system_name,
                str(error)
            )

    # ==================================================
    # PROJECT FOLDER
    # ==================================================

    def open_project_folder(self):

        self.write_log(
            "PROJECT FOLDER ditekan."
        )

        try:

            project_folder = (
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(
                            __file__
                        )
                    )
                )
            )

            os.startfile(
                project_folder
            )

        except Exception as error:

            self.write_log(
                "Gagal membuka folder proyek: "
                + str(error)
            )

            messagebox.showerror(
                self.system_name,
                str(error)
            )

    # ==================================================
    # VIEW LOG
    # ==================================================

    def view_log(self):

        if (
            self.log_window
            and
            self.log_window.winfo_exists()
        ):

            self.log_window.destroy()

            self.log_window = None

            self.write_log(
                "VIEW LOG ditutup."
            )

            return

        self.log_window = tk.Toplevel(
            self.root
        )

        self.log_window.title(
            "SYSTEM LOG"
        )

        self.log_window.geometry(
            "850x500"
        )

        self.log_window.configure(
            bg=self.background_color
        )

        self.log_window.protocol(
            "WM_DELETE_WINDOW",
            self.close_log_window
        )

        text_frame = tk.Frame(
            self.log_window,
            bg=self.background_color
        )

        text_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.log_display = tk.Text(
            text_frame,
            bg=self.dark_color,
            fg="#E5E7EB",
            font=("Consolas", 10),
            relief="flat",
            padx=12,
            pady=12
        )

        self.log_display.pack(
            fill="both",
            expand=True
        )

        bottom = tk.Frame(
            self.log_window,
            bg=self.background_color
        )

        bottom.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        tk.Button(
            bottom,
            text="REFRESH",
            command=self.refresh_log_window,
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            bottom,
            text="CLEAR VIEW",
            command=self.clear_log_view,
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            bottom,
            text="CLOSE",
            command=self.close_log_window,
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=5
        )

        self.refresh_log_window()

        self.write_log(
            "VIEW LOG dibuka."
        )

    def refresh_log_window(self):

        if not self.log_window:

            return

        if not self.log_window.winfo_exists():

            return

        self.log_display.configure(
            state="normal"
        )

        self.log_display.delete(
            "1.0",
            "end"
        )

        for line in self.system_logs:

            self.log_display.insert(
                "end",
                line + "\n"
            )

        self.log_display.see(
            "end"
        )

        self.log_display.configure(
            state="disabled"
        )

    def clear_log_view(self):

        if not self.log_window:

            return

        self.log_display.configure(
            state="normal"
        )

        self.log_display.delete(
            "1.0",
            "end"
        )

        self.log_display.configure(
            state="disabled"
        )

    def close_log_window(self):

        if self.log_window:

            self.log_window.destroy()

            self.log_window = None

            self.write_log(
                "VIEW LOG ditutup."
            )

    # ==================================================
    # LOGOUT
    # ==================================================

    def logout(self):

        if self.is_logging_out:

            return

        confirm = messagebox.askyesno(
            "Konfirmasi Logout",
            "Apakah Anda yakin ingin keluar dari akun ini?"
        )

        if not confirm:

            return

        self.is_logging_out = True

        self.write_log(
            "User melakukan logout."
        )

        if self.on_logout_callback:

            self.on_logout_callback()

    # ==================================================
    # CLOSE APPLICATION
    # ==================================================

    def handle_close(self):

        if self.is_closing:

            return

        confirm = messagebox.askyesno(
            "Tutup SATRIA MAS",
            "Apakah Anda yakin ingin menutup aplikasi?"
        )

        if not confirm:

            return

        self.is_closing = True

        self.write_log(
            "Permintaan penutupan aplikasi diterima."
        )

        if self.on_close_callback:

            self.on_close_callback()

            return

        else:

            self.root.destroy()

    # ==================================================
    # RUN
    # ==================================================

    def run(self):

        self.root.mainloop()