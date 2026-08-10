import os
import time
import tkinter as tk

from login_window import LoginWindow
from dashboard_window import DashboardWindow
from services.system_controller import system_controller

# Deteksi otomatis apakah berjalan di server cloud (Railway / Headless)
IS_CLOUD = os.environ.get("PORT") is not None or os.environ.get("RAILWAY_ENVIRONMENT") is not None or os.environ.get("CI") is not None

class TerataiLauncher:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self):
        self.is_closing = False
        
        if IS_CLOUD:
            print("=" * 60)
            print("[LAUNCHER] Terdeteksi berjalan di Server Cloud (Headless Mode)")
            print("[LAUNCHER] Melewati inisialisasi GUI Tkinter...")
            print("=" * 60)
            self.root = None
            self.current_window = None
            self.run_cloud_backend()
        else:
            # Mode Normal untuk Komputer Lokal (Desktop GUI)
            self.root = tk.Tk()
            self.root.withdraw()
            self.current_window = None
            self.show_login()

    # ==================================================
    # CLOUD BACKEND RUNNER (Pengganti GUI di Server)
    # ==================================================

    def run_cloud_backend(self):
        """Menjalankan sistem secara otomatis di latar belakang tanpa layar/monitor."""
        try:
            print("[LAUNCHER] Memulai protokol START SYSTEM di Cloud...")
            system_controller.start_system()
            print("[LAUNCHER] Sistem Cloud aktif dan berjalan 24 jam.")
        except Exception as error:
            print(f"[LAUNCHER] Error saat memulai sistem cloud: {error}")

        # Loop abadi agar kontainer cloud tidak tertutup / berhenti
        try:
            while not self.is_closing:
                time.sleep(3600)
        except KeyboardInterrupt:
            self.close_application()

    # ==================================================
    # LOGIN
    # ==================================================

    def show_login(self):
        if IS_CLOUD:
            return
        self.close_current_window()
        self.current_window = LoginWindow(
            self.root,
            on_login_success=self.login_success
        )
        self.current_window.root.deiconify()

    # ==================================================
    # LOGIN SUCCESS
    # ==================================================

    def login_success(self, user):
        if IS_CLOUD:
            return
        print("=" * 50)
        print("LOGIN BERHASIL")
        print("Username :", user["username"])
        print("Role     :", user["role"])
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
        if IS_CLOUD or self.is_closing:
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
            print("[LAUNCHER] Memulai protokol STOP SYSTEM.")
            success = system_controller.close_system()
            if success:
                print("[LAUNCHER] STOP SYSTEM berhasil.")
            else:
                print("[LAUNCHER] STOP SYSTEM selesai dengan peringatan.")
        except Exception as error:
            print("[LAUNCHER] Error STOP SYSTEM:", error)
        finally:
            print("[LAUNCHER] STOP SYSTEM selesai.")
            self.close_current_window()
            
            if not IS_CLOUD and self.root:
                print("[LAUNCHER] Menghentikan mainloop.")
                try:
                    self.root.quit()
                    self.root.destroy()
                except Exception:
                    pass

            print("[LAUNCHER] Aplikasi ditutup.")

    # ==================================================
    # CLOSE CURRENT WINDOW
    # ==================================================

    def close_current_window(self):
        if IS_CLOUD:
            return
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
        if not IS_CLOUD and self.root:
            self.root.mainloop()


# ======================================================
# ENTRY POINT
# ======================================================

if __name__ == "__main__":
    app = TerataiLauncher()
    app.run()