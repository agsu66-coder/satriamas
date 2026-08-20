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
    
        # 1. Jalankan Server HTTP Railway (Port Dinamis) di Thread Terpisah
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

        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()

        # 2. Jalankan app.py dan pantau log secara aman tanpa memblokir server utama
        import subprocess
        import queue

        def enqueue_output(out, queue_obj):
            for line in iter(out.readline, b''):
                queue_obj.put(line.decode('utf-8', errors='ignore'))
            out.close()

        def run_bot_sequence():
            print("[LAUNCHER] Menjalankan app.py (Python) di background...")
            try:
                process = subprocess.Popen(
                    ["python", "app.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                )

                q = queue.Queue()
                t = threading.Thread(target=enqueue_output, args=(process.stdout, q), daemon=True)
                t.start()

                node_started = False

                # Loop pemantauan non-blocking
                while True:
                    try:
                        line = q.get_nowait()
                    except queue.Empty:
                        # Jika belum ada log baru, beri jeda singkat agar CPU tidak tinggi
                        time.sleep(0.1)
                        if process.poll() is not None:
                            break
                        continue

                    cleaned_line = line.strip()
                    if cleaned_line:
                        print(f"[app.py] {cleaned_line}")

                        # Begitu teks penanda siap muncul, jalankan index.js sekali saja
                        if not node_started and ("Running on" in cleaned_line or "5000" in cleaned_line):
                            node_started = True
                            print("[LAUNCHER] Terdeteksi app.py siap! Menjalankan index.js...")
                            subprocess.Popen(["node", "index.js"])
                            print("[LAUNCHER] index.js berhasil dimulai.")

            except Exception as e:
                print(f"[LAUNCHER] Error pada urutan bot: {e}")

        # Jalankan urutan bot di thread independen
        bot_thread = threading.Thread(target=run_bot_sequence, daemon=True)
        bot_thread.start()

        # 3. Pertahankan agar kontainer utama tetap menyala 24 jam penuh
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