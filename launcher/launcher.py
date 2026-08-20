import os
import http.server
import socketserver
import threading
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
        print("[LAUNCHER] Menjalankan server HTTP dummy untuk merespons Railway Health Check...")
    
        # Ambil port yang disediakan oleh Railway, default ke 8080 jika lokal
        PORT = int(os.environ.get("PORT", 8080))
    
        class SimpleHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Teratai Bot is running 24/7 successfully!")
            
            def log_message(self, format, *args):
                return # Mencegah spam log HTTP berlebih

        def start_server():
            with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
                print(f"[LAUNCHER] HTTP Server aktif pada port {PORT}")
                httpd.serve_forever()

        # 1. Jalankan server HTTP di latar belakang (daemon thread)
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

        # 2. MENJALANKAN app.py DAN MENUNGGU TEKS PENANDA
        import subprocess
        
        def monitor_and_start_node():
            print("[LAUNCHER] Menjalankan app.py (Python) dan memantau log-nya...")
            try:
                # Jalankan app.py dan tangkap output-nya secara real-time
                process = subprocess.Popen(
                    ["python", "app.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                # Baca output baris demi baris dari app.py
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(f"[app.py] {output.strip()}")
                        
                        # Periksa apakah teks penanda sudah muncul
                        if "Running on" in output or "5000" in output:
                            print("[LAUNCHER] Terdeteksi app.py sudah siap! Menjalankan index.js...")
                            
                            # Jalankan index.js setelah app.py siap
                            subprocess.Popen(["node", "index.js"])
                            print("[LAUNCHER] index.js berhasil dimulai.")
                            break # Keluar dari pemantauan setelah index.js dijalankan
            except Exception as e:
                print(f"[LAUNCHER] Error saat memantau app.py: {e}")

        # Jalankan fungsi pemantauan di latar belakang agar tidak memblokir server HTTP
        monitor_thread = threading.Thread(target=monitor_and_start_node, daemon=True)
        monitor_thread.start()

        # 3. Biarkan proses utama terus menyala 24 jam
        while True:
            time.sleep(60)

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