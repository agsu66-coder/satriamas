import os
import sys
import time
import signal
import socket
import subprocess
import threading
from datetime import datetime


class SystemController:

    # ==================================================
    # KONFIGURASI
    # ==================================================

    BACKEND_HOST = "127.0.0.1"
    BACKEND_PORT = 5000

    BACKEND_DIR_NAME = "backend"
    BOT_DIR_NAME = "bot"

    BACKEND_FILE = "app.py"
    BOT_FILE = "index.js"

    # ==================================================
    # STATE SISTEM
    # ==================================================

    OFFLINE = "OFFLINE"
    STARTING = "STARTING"
    ONLINE = "ONLINE"
    STOPPING = "STOPPING"
    STANDBY = "STANDBY"
    RESTARTING = "RESTARTING"
    CHECKING = "CHECKING"
    CLOSING = "CLOSING"

    # ==================================================
    # INIT
    # ==================================================

    def __init__(self, logger=None):

        self.logger = logger

        self.backend_process = None

        self.bot_process = None

        self.system_state = self.OFFLINE

        self.operation_in_progress = False

        self.operation_name = None

        self.lock = threading.Lock()

        self.base_dir = self.get_base_dir()

        self.backend_dir = os.path.join(

            self.base_dir,

            self.BACKEND_DIR_NAME

        )

        self.bot_dir = os.path.join(

            self.base_dir,

            self.BOT_DIR_NAME

        )

        self.backend_file = os.path.join(

            self.backend_dir,

            self.BACKEND_FILE

        )

        self.bot_file = os.path.join(

            self.bot_dir,

            self.BOT_FILE

        )

    # ==================================================
    # BASE DIRECTORY
    # ==================================================

    def get_base_dir(self):

        """

        Struktur:

        v0.2/
        │
        ├── backend/
        │   └── app.py
        │
        ├── bot/
        │   └── index.js
        │
        └── launcher/
            └── services/
                └── system_controller.py

        """

        return os.path.abspath(

            os.path.join(

                os.path.dirname(__file__),

                "..",

                ".."

            )

        )

    # ==================================================
    # LOGGER
    # ==================================================

    def log(self, message):

        timestamp = datetime.now().strftime(

            "%H:%M:%S"

        )

        text = f"[{timestamp}] {message}"

        print(text)

        if self.logger:

            try:

                self.logger(text)

            except Exception:

                pass

    # ==================================================
    # STATE
    # ==================================================

    def get_state(self):

        return self.system_state

    # ==================================================
    # OPERATION LOCK
    # ==================================================

    def begin_operation(self, operation):

        with self.lock:

            if self.operation_in_progress:

                self.log(

                    f"OPERASI DITOLAK. "

                    f"Sedang menjalankan: "

                    f"{self.operation_name}"

                )

                return False

            self.operation_in_progress = True

            self.operation_name = operation

            return True

    # ==================================================

    def end_operation(self):

        with self.lock:

            self.operation_in_progress = False

            self.operation_name = None

    # ==================================================
    # VALIDASI PROSES
    # ==================================================

    def is_backend_running(self):

        return (

            self.backend_process is not None

            and

            self.backend_process.poll() is None

        )

    # ==================================================

    def is_bot_running(self):

        return (

            self.bot_process is not None

            and

            self.bot_process.poll() is None

        )

    # ==================================================
    # VALIDASI PORT BACKEND
    # ==================================================

    def is_backend_port_open(self):

        try:

            with socket.create_connection(

                (

                    self.BACKEND_HOST,

                    self.BACKEND_PORT

                ),

                timeout=1

            ):

                return True

        except OSError:

            return False

    # ==================================================
    # MENUNGGU PORT TERBUKA
    # ==================================================

    def wait_backend_ready(

        self,

        timeout=60

    ):

        start_time = time.time()

        while (

            time.time() - start_time

            <

            timeout

        ):

            if self.is_backend_port_open():

                return True

            time.sleep(1)

        return False

    def stop_backend_by_port(self):

        self.log(
            "Mencari PID yang menggunakan port backend."
        )

        try:

            result = subprocess.run(

                [

                    "netstat",

                    "-ano"

                ],

                capture_output=True,

                text=True,

                creationflags=subprocess.CREATE_NO_WINDOW

            )

            pids = set()

            for line in result.stdout.splitlines():

                if (

                    f":{self.BACKEND_PORT}"

                    in line

                    and

                    "LISTENING"

                    in line

                ):

                    parts = line.split()

                    if not parts:

                        continue

                    pid = parts[-1]

                    if pid.isdigit():

                        pids.add(pid)

            if not pids:

                self.log(

                    "Tidak ditemukan PID untuk port backend."

                )

                return False

            for pid in pids:

                self.log(

                    f"Menghentikan proses PID {pid}."

                )

                subprocess.run(

                    [

                        "taskkill",

                        "/PID",

                        pid,

                        "/T",

                        "/F"

                    ],

                    capture_output=True,

                    text=True,

                    creationflags=subprocess.CREATE_NO_WINDOW

                )

            time.sleep(2)

            if self.is_backend_port_open():

                self.log(

                    "Port backend masih aktif."

                )

                return False

            self.log(

                "Port backend berhasil ditutup."

            )

            return True

        except Exception as error:

            self.log(

                f"Gagal menghentikan proses berdasarkan port: {error}"

            )

            return False

    # ==================================================
    # MENUNGGU PORT TERTUTUP
    # ==================================================

    def wait_backend_stopped(

        self,

        timeout=30

    ):

        start_time = time.time()

        while (

            time.time() - start_time

            <

            timeout

        ):

            if not self.is_backend_port_open():

                return True

            time.sleep(1)

        return False

    # ==================================================
    # START BACKEND
    # ==================================================

    def start_backend(self):

        if self.is_backend_running():

            self.log(

                "Backend sudah berjalan."

            )

            return True

        if self.is_backend_port_open():

            self.log(

                "Port backend sudah aktif."

            )

            return True

        if not os.path.exists(

            self.backend_file

        ):

            self.log(

                "ERROR: app.py tidak ditemukan."

            )

            return False

        self.log(

            "Memulai Backend app.py."

        )

        try:

            creationflags = 0

            if sys.platform == "win32":

                creationflags = (

                    subprocess.CREATE_NEW_PROCESS_GROUP

                )

            self.backend_process = subprocess.Popen(

                [

                    sys.executable,

                    self.backend_file

                ],

                cwd=self.backend_dir,

                creationflags=creationflags

            )

            self.log(

                "Proses backend berhasil dibuat."

            )

            self.log(

                "Menunggu backend pada "

                f"{self.BACKEND_HOST}:"

                f"{self.BACKEND_PORT}..."

            )

            ready = self.wait_backend_ready()

            if not ready:

                self.log(

                    "ERROR: Backend tidak siap."

                )

                return False

            self.log(

                "Backend siap menerima koneksi."

            )

            return True

        except Exception as err:

            self.log(

                f"ERROR START BACKEND: {err}"

            )

            return False

    # ==================================================
    # START BOT
    # ==================================================

    def start_bot(self):

        if self.is_bot_running():

            self.log(

                "Bot sudah berjalan."

            )

            return True

        if not os.path.exists(

            self.bot_file

        ):

            self.log(

                "ERROR: index.js tidak ditemukan."

            )

            return False

        self.log(

            "Memulai WhatsApp Bot."

        )

        try:

            creationflags = 0

            if sys.platform == "win32":

                creationflags = (

                    subprocess.CREATE_NEW_PROCESS_GROUP

                )

            self.bot_process = subprocess.Popen(

                [

                    "node",

                    self.BOT_FILE

                ],

                cwd=self.bot_dir,

                creationflags=creationflags

            )

            self.log(

                "Proses WhatsApp Bot berhasil dibuat."

            )

            return True

        except Exception as err:

            self.log(

                f"ERROR START BOT: {err}"

            )

            return False

    # ==================================================
    # START SYSTEM
    # ==================================================

    def start_system(self):

        if not self.begin_operation(

            "START SYSTEM"

        ):

            return False

        try:

            self.system_state = self.STARTING

            self.log(

                "Memulai START SYSTEM."

            )

            # ------------------------------------------
            # JIKA BACKEND BELUM AKTIF
            # ------------------------------------------

            if not self.is_backend_running():

                if not self.start_backend():

                    self.system_state = self.OFFLINE

                    return False

            else:

                self.log(

                    "Backend sudah aktif."

                )

            # ------------------------------------------
            # START BOT
            # ------------------------------------------

            if not self.start_bot():

                self.system_state = self.STANDBY

                return False

            self.system_state = self.ONLINE

            self.log(

                "START SYSTEM BERHASIL."

            )

            return True

        finally:

            self.end_operation()

    # ==================================================
    # STOP BOT
    # ==================================================

    def stop_bot(self):

        if not self.begin_operation(

            "STOP BOT"

        ):

            return False

        try:

            self.system_state = self.STOPPING

            self.log(

                "Memulai STOP BOT."

            )

            if not self.is_bot_running():

                self.log(

                    "Bot tidak sedang berjalan."

                )

                self.system_state = self.STANDBY

                return True

            self.log(

                "Mengirim sinyal penghentian Bot."

            )

            try:

                if sys.platform == "win32":

                    self.bot_process.send_signal(

                        signal.CTRL_BREAK_EVENT

                    )

                else:

                    self.bot_process.terminate()

            except Exception as err:

                self.log(

                    f"Graceful stop gagal: {err}"

                )

            # ------------------------------------------
            # TUNGGU BOT
            # ------------------------------------------

            self.log(

                "Menunggu Bot berhenti."

            )

            try:

                self.bot_process.wait(

                    timeout=30

                )

            except subprocess.TimeoutExpired:

                self.log(

                    "Bot tidak berhenti normal."

                )

                self.log(

                    "Memaksa penghentian Bot."

                )

                self.bot_process.kill()

                self.bot_process.wait()

            self.bot_process = None

            self.system_state = self.STANDBY

            self.log(

                "STOP BOT BERHASIL."

            )

            return True

        finally:

            self.end_operation()

    # ==================================================
    # RESTART BOT
    # ==================================================

    def restart_bot(self):

        if not self.begin_operation(

            "RESTART BOT"

        ):

            return False

        try:

            self.system_state = self.RESTARTING

            self.log(

                "Memulai RESTART BOT."

            )

            # ------------------------------------------
            # STOP BOT
            # ------------------------------------------

            if self.is_bot_running():

                self.log(

                    "Menghentikan Bot lama."

                )

                try:

                    if sys.platform == "win32":

                        self.bot_process.send_signal(

                            signal.CTRL_BREAK_EVENT

                        )

                    else:

                        self.bot_process.terminate()

                except Exception as err:

                    self.log(

                        f"Gagal mengirim stop: {err}"

                    )

                try:

                    self.bot_process.wait(

                        timeout=30

                    )

                except subprocess.TimeoutExpired:

                    self.log(

                        "Bot tidak berhenti normal."

                    )

                    self.bot_process.kill()

                    self.bot_process.wait()

                self.bot_process = None

            else:

                self.log(

                    "Bot sudah tidak berjalan."

                )

            # ------------------------------------------
            # VALIDASI BACKEND
            # ------------------------------------------

            if not self.is_backend_port_open():

                self.log(

                    "Backend tidak aktif."

                )

                self.log(

                    "Menyalakan backend."

                )

                if not self.start_backend():

                    self.system_state = self.OFFLINE

                    return False

            else:

                self.log(

                    "Backend masih aktif."

                )

            # ------------------------------------------
            # START BOT
            # ------------------------------------------

            if not self.start_bot():

                self.system_state = self.STANDBY

                return False

            self.system_state = self.ONLINE

            self.log(

                "RESTART BOT BERHASIL."

            )

            return True

        finally:

            self.end_operation()

    # ==================================================
    # CHECK SYSTEM
    # ==================================================

    def check_system(self):

        if not self.begin_operation(

            "CHECK SYSTEM"

        ):

            return None

        try:

            previous_state = self.system_state

            self.system_state = self.CHECKING

            self.log(

                "Memulai CHECK SYSTEM."

            )

            result = {

                "backend_process": self.is_backend_running(),

                "backend_port": self.is_backend_port_open(),

                "bot_process": self.is_bot_running(),

                "backend_file": os.path.exists(

                    self.backend_file

                ),

                "bot_file": os.path.exists(

                    self.bot_file

                ),

                "state_before_check": previous_state

            }

            # ------------------------------------------
            # ANALISIS STATUS
            # ------------------------------------------

            if (

                result["backend_process"]

                and

                result["backend_port"]

                and

                result["bot_process"]

            ):

                result["system"] = "ONLINE"

            elif (

                result["backend_process"]

                and

                result["backend_port"]

                and

                not result["bot_process"]

            ):

                result["system"] = "STANDBY"

            else:

                result["system"] = "OFFLINE"

            self.system_state = result["system"]

            self.log(

                "CHECK SYSTEM selesai."

            )

            return result

        finally:

            self.end_operation()

    # =====================================================
    # GET STATUS
    # =====================================================

    def get_status(self):

        """
        Mengambil status terkini sistem
        untuk kebutuhan Dashboard.

        Tidak menjalankan START,
        STOP,
        RESTART,
        atau perubahan proses apa pun.

        Hanya membaca kondisi aktual.
        """

        result = self.check_system()

        backend_status = (

            "ONLINE"

            if (

                result.get(

                    "backend_port",

                    False

                )

                and

                result.get(

                    "backend_ready",

                    False

                )

            )

            else

            "OFFLINE"

        )

        bot_status = (

            "ONLINE"

            if result.get(

                "bot_process",

                False

            )

            else

            "OFFLINE"

        )

        internet_status = (

            "ONLINE"

            if result.get(

                "internet_available",

                False

            )

            else

            "OFFLINE"

        )

        return {

            "backend": backend_status,

            "bot_process": bot_status,

            "whatsapp_connection": bot_status,

            "internet": internet_status,

            "database": "READY",

            "system": result.get(

                "system",

                "OFFLINE"

            )

        }
    # ==================================================
    # CLOSE SYSTEM
    # ==================================================

    def close_system(self):

        if not self.begin_operation(

            "CLOSE SYSTEM"

        ):

            return False

        try:

            self.system_state = self.CLOSING

            self.log(

                "Memulai CLOSE SYSTEM."

            )

            # ------------------------------------------
            # STOP BOT
            # ------------------------------------------

            if self.is_bot_running():

                self.log(

                    "Menghentikan WhatsApp Bot."

                )

                try:

                    if sys.platform == "win32":

                        self.bot_process.send_signal(

                            signal.CTRL_BREAK_EVENT

                        )

                    else:

                        self.bot_process.terminate()

                except Exception as err:

                    self.log(

                        f"Gagal menghentikan Bot: {err}"

                    )

                try:

                    self.bot_process.wait(

                        timeout=30

                    )

                except subprocess.TimeoutExpired:

                    self.log(

                        "Memaksa penghentian Bot."

                    )

                    self.bot_process.kill()

                    self.bot_process.wait()

                self.bot_process = None

                self.log(

                    "WhatsApp Bot berhenti."

                )

            else:

                self.log(

                    "Bot tidak sedang dikendalikan launcher."

                )

            # ------------------------------------------
            # STOP BACKEND
            # ------------------------------------------

            if self.is_backend_running():

                self.log(

                    "Menghentikan Backend."

                )

                try:

                    if sys.platform == "win32":

                        self.backend_process.send_signal(

                            signal.CTRL_BREAK_EVENT

                        )

                    else:

                        self.backend_process.terminate()

                except Exception as err:

                    self.log(

                        f"Gagal menghentikan Backend: {err}"

                    )

                try:

                    self.backend_process.wait(

                        timeout=30

                    )

                except subprocess.TimeoutExpired:

                    self.log(

                        "Memaksa penghentian Backend."

                    )

                    self.backend_process.kill()

                    self.backend_process.wait()

                self.backend_process = None

            else:

                self.log(

                    "Backend tidak sedang dikendalikan launcher."

                )

                # ------------------------------------------
                # FALLBACK: CEK PORT BACKEND
                # ------------------------------------------

                if self.is_backend_port_open():

                    self.log(

                        "Port 5000 masih aktif."

                    )

                    self.log(

                        "Mencari proses yang menggunakan port 5000."

                    )

                    self.stop_backend_by_port()

                else:

                    self.log(

                        "Port 5000 sudah tertutup."

                    )

            # ------------------------------------------
            # PORT HARUS TERTUTUP
            # ------------------------------------------

            self.log(

                "Menunggu port backend tertutup."

            )

            if self.wait_backend_stopped():

                self.log(

                    "Port backend sudah tertutup."

                )

            else:

                self.log(

                    "PERINGATAN: Port backend masih terbuka."

                )

            self.system_state = self.OFFLINE

            self.log(

                "CLOSE SYSTEM BERHASIL."

            )

            return True

        finally:

            self.end_operation()


# ======================================================
# SINGLETON
# ======================================================

system_controller = SystemController()