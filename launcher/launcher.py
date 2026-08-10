import tkinter as tk

from login_window import LoginWindow
from dashboard_window import DashboardWindow

from services.system_controller import system_controller


class TerataiLauncher:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self):

        self.root = tk.Tk()

        self.root.withdraw()

        self.current_window = None

        self.is_closing = False

        self.show_login()

    # ==================================================
    # LOGIN
    # ==================================================

    def show_login(self):

        self.close_current_window()

        self.current_window = LoginWindow(

            self.root,

            on_login_success=self.login_success

        )

        self.current_window.root.deiconify()

    # ==================================================
    # LOGIN SUCCESS
    # ==================================================

    def login_success(

        self,

        user

    ):

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

        self.close_current_window()

        self.current_window = DashboardWindow(

            current_user=user,

            on_logout=self.logout,

            on_close=self.close_application

        )

        self.current_window.root.deiconify()

    # ==================================================
    # LOGOUT
    # ==================================================

    def logout(self):

        if self.is_closing:

            return

        print("=" * 50)

        print("LOGOUT")

        print("=" * 50)

        self.close_current_window()

        self.show_login()

    # ==================================================
    # CLOSE APPLICATION
    # ==================================================

    def close_application(self):

        if self.is_closing:

            return

        self.is_closing = True

        print("=" * 60)

        print("CLOSING TERATAI AI")

        print("=" * 60)

        try:

            print(

                "[LAUNCHER] Memulai protokol STOP SYSTEM."

            )

            success = (

                system_controller

                .close_system()

            )

            if success:

                print(

                    "[LAUNCHER] STOP SYSTEM berhasil."

                )

            else:

                print(

                    "[LAUNCHER] STOP SYSTEM selesai "

                    "dengan peringatan."

                )

        except Exception as error:

            print(

                "[LAUNCHER] Error STOP SYSTEM:",

                error

            )

        finally:

            print(

                "[LAUNCHER] STOP SYSTEM selesai."
            )

            self.close_current_window()

            print(

                "[LAUNCHER] Menghentikan mainloop."

            )

            self.root.quit()

            self.root.destroy()

            print(

                "[LAUNCHER] Aplikasi ditutup."

            )

    # ==================================================
    # CLOSE CURRENT WINDOW
    # ==================================================

    def close_current_window(self):

        if self.current_window:

            try:

                self.current_window.root.destroy()

            except Exception:

                pass

            self.current_window = None

    # ==================================================
    # RUN
    # ==================================================

    def run(self):

        self.root.mainloop()


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":

    app = TerataiLauncher()

    app.run()