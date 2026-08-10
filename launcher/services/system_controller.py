import os
import sys
import time
import socket
import subprocess
import threading
import urllib.request
import json
import signal


class SystemController:

    # =====================================================
    # KONFIGURASI
    # =====================================================

    BACKEND_HOST = "127.0.0.1"
    BACKEND_PORT = 5000

    # =====================================================
    # STATE
    # =====================================================

    OFFLINE = "OFFLINE"
    STARTING = "STARTING"
    ONLINE = "ONLINE"
    STOPPING = "STOPPING"
    BACKEND_ONLY = "BACKEND_ONLY"
    RESTARTING = "RESTARTING"
    CHECKING = "CHECKING"
    CLOSING = "CLOSING"
    INTERNET_OFFLINE = "INTERNET_OFFLINE"

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        # -------------------------------------------------
        # ROOT PROJECT
        # -------------------------------------------------

        self.base_dir = os.path.abspath(

            os.path.join(

                os.path.dirname(__file__),

                "..",

                ".."

            )

        )

        # -------------------------------------------------
        # BACKEND
        # -------------------------------------------------

        self.backend_dir = os.path.join(

            self.base_dir,

            "backend"

        )

        self.backend_file = os.path.join(

            self.backend_dir,

            "app.py"

        )

        # -------------------------------------------------
        # BOT
        # -------------------------------------------------

        self.bot_dir = os.path.join(

            self.base_dir,

            "bot"

        )

        self.bot_file = os.path.join(

            self.bot_dir,

            "index.js"

        )

        # -------------------------------------------------
        # HEALTH
        # -------------------------------------------------

        self.health_url = (

            f"http://"

            f"{self.BACKEND_HOST}:"

            f"{self.BACKEND_PORT}"

            "/health"

        )

        # -------------------------------------------------
        # PROCESS REFERENCE
        # -------------------------------------------------

        self.backend_process = None

        self.bot_process = None

        # -------------------------------------------------
        # STATE
        # -------------------------------------------------

        self.state = self.OFFLINE

        # -------------------------------------------------
        # LOCK
        # -------------------------------------------------

        self.control_lock = threading.Lock()

        self.operation = None

        self.log_callback = None

    # =====================================================
    # LOGGER
    # =====================================================

    def log(self, message):

        timestamp = time.strftime(
            "%H:%M:%S"
        )

        formatted_message = (
            f"[{timestamp}] {message}"
        )

        # ---------------------------------------------
        # CONSOLE LOG
        # ---------------------------------------------

        print(
            formatted_message
        )

        # ---------------------------------------------
        # DASHBOARD LOG
        # ---------------------------------------------

        if self.log_callback:

            try:

                self.log_callback(
                    formatted_message
                )

            except Exception as error:

                print(
                    "[LOG CALLBACK ERROR]",
                    error
                )

    def set_log_callback(
        self,
        callback
    ):

        self.log_callback = callback

    # =====================================================
    # FILE VALIDATION
    # =====================================================

    def backend_file_exists(self):

        return os.path.isfile(

            self.backend_file

        )

    def bot_file_exists(self):

        return os.path.isfile(

            self.bot_file

        )

    # =====================================================
    # BACKEND PROCESS - INTERNAL REFERENCE
    # =====================================================

    def is_backend_process_running(self):

        return (

            self.backend_process is not None

            and

            self.backend_process.poll() is None

        )

    # =====================================================
    # BOT PROCESS - INTERNAL REFERENCE
    # =====================================================

    def is_bot_process_running(self):

        if (

            self.bot_process is not None

            and

            self.bot_process.poll() is None

        ):

            return True

        return False

    # =====================================================
    # BOT PROCESS - SYSTEM DETECTION
    # =====================================================
    # =====================================================
    # BOT PROCESS - SYSTEM DETECTION
    # =====================================================

    def get_bot_pids(self):

        """
        Mendeteksi PID proses Node.js yang menjalankan
        bot/index.js TERATAI AI.

        Tidak bergantung pada:

            self.bot_process

        sehingga tetap dapat mendeteksi bot yang dijalankan
        oleh instance Python sebelumnya.

        Tidak menggunakan nama node.exe pada CommandLine,
        karena CommandLine aktual dapat berbentuk:

            node "E:\\Teratai Proyek\\v0.2\\bot\\index.js"

        Identitas utama adalah path index.js TERATAI.
        """

        pids = []

        try:

            command = [

                "wmic",

                "process",

                "where",

                "name='node.exe'",

                "get",

                "ProcessId,CommandLine",

                "/format:csv"

            ]

            result = subprocess.run(

                command,

                capture_output=True,

                text=True,

                encoding="utf-8",

                errors="ignore"

            )

            target = os.path.normcase(

                os.path.normpath(

                    self.bot_file

                )

            )

            for line in result.stdout.splitlines():

                line = line.strip()

                if not line:

                    continue

                lower_line = os.path.normcase(

                    line

                )

                # -----------------------------------------
                # CUKUP mencari path index.js TERATAI
                # -----------------------------------------

                if target not in lower_line:

                    continue

                # -----------------------------------------
                # Ambil PID dari kolom terakhir
                # -----------------------------------------

                parts = line.split(",")

                if len(parts) < 2:

                    continue

                try:

                    pid = int(

                        parts[-1].strip()

                    )

                    pids.append(pid)

                except ValueError:

                    continue

        except Exception as err:

            self.log(

                f"Gagal mendeteksi proses bot: {err}"

            )

        return list(

            set(pids)

        )

    # =====================================================
    # PROCESS TREE
    # =====================================================

    def get_process_tree(self, root_pid):

        """

        Mendapatkan seluruh child process

        dari PID utama bot.

        """

        tree = set()

        try:

            command = [

                "wmic",

                "process",

                "get",

                "ProcessId,ParentProcessId",

                "/format:csv"

            ]

            result = subprocess.run(

                command,

                capture_output=True,

                text=True,

                encoding="utf-8",

                errors="ignore"

            )

            parent_map = {}

            for line in result.stdout.splitlines():

                line = line.strip()

                if not line:

                    continue

                parts = line.split(",")

                if len(parts) < 3:

                    continue

                try:

                    parent_pid = int(

                        parts[-2].strip()

                    )

                    pid = int(

                        parts[-1].strip()

                    )

                    parent_map.setdefault(

                        parent_pid,

                        []

                    ).append(pid)

                except ValueError:

                    continue

            queue = [root_pid]

            while queue:

                current = queue.pop(0)

                if current in tree:

                    continue

                tree.add(current)

                children = parent_map.get(

                    current,

                    []

                )

                queue.extend(children)

        except Exception as err:

            self.log(

                f"Gagal membaca process tree: {err}"

            )

            tree.add(root_pid)

        return list(tree)

    # =====================================================
    # STOP PROCESS TREE
    # =====================================================

    def stop_bot_process_tree(self):

        """

        Menghentikan:

        node index.js

        beserta child process-nya.

        Tidak menghentikan node.exe lain.

        """

        bot_pids = self.get_bot_pids()

        if not bot_pids:

            self.log(

                "Proses WhatsApp Bot tidak ditemukan."

            )

            self.bot_process = None

            return True

        all_pids = set()

        for pid in bot_pids:

            tree = self.get_process_tree(

                pid

            )

            all_pids.update(tree)

        self.log(

            f"Process tree Bot ditemukan: "

            f"{sorted(all_pids)}"

        )

        success = True

        # Hentikan dari child terlebih dahulu

        for pid in sorted(

            all_pids,

            reverse=True

        ):

            try:

                result = subprocess.run(

                    [

                        "taskkill",

                        "/PID",

                        str(pid),

                        "/T",

                        "/F"

                    ],

                    capture_output=True,

                    text=True,

                    encoding="utf-8",

                    errors="ignore"

                )

                if result.returncode != 0:

                    # Proses mungkin sudah mati

                    pass

            except Exception as err:

                self.log(

                    f"Gagal menghentikan PID "

                    f"{pid}: {err}"

                )

                success = False

        # Tunggu proses benar-benar hilang

        timeout = 30

        start_time = time.time()

        while (

            time.time()

            -

            start_time

            <

            timeout

        ):

            remaining = self.get_bot_pids()

            if not remaining:

                self.bot_process = None

                self.log(

                    "Process tree WhatsApp Bot "

                    "berhasil dihentikan."

                )

                return success

            time.sleep(1)

        self.log(

            "Timeout menunggu process tree Bot."

        )

        return False

    # =====================================================
    # BACKEND PORT
    # =====================================================

    def is_backend_port_open(self):

        sock = socket.socket(

            socket.AF_INET,

            socket.SOCK_STREAM

        )

        sock.settimeout(1)

        try:

            result = sock.connect_ex(

                (

                    self.BACKEND_HOST,

                    self.BACKEND_PORT

                )

            )

            return result == 0

        except Exception:

            return False

        finally:

            sock.close()

    # =====================================================
    # BACKEND READY
    # =====================================================

    def is_backend_ready(self):

        try:

            response = urllib.request.urlopen(

                self.health_url,

                timeout=2

            )

            return response.status == 200

        except Exception:

            return False

    # =====================================================
    # INTERNET STATUS
    # =====================================================

    def is_internet_available(self):

        test_urls = [

            "https://www.google.com",

            "https://www.cloudflare.com",

            "https://www.microsoft.com"

        ]

        for url in test_urls:

            try:

                request = urllib.request.Request(

                    url,

                    method="HEAD",

                    headers={

                        "User-Agent":

                        "TERATAI-AI-Monitor"

                    }

                )

                with urllib.request.urlopen(

                    request,

                    timeout=3

                ) as response:

                    if response.status < 500:

                        return True

            except Exception:

                continue

        return False




    # =====================================================
    # START BACKEND
    # =====================================================

    def start_backend(self):

        if self.is_backend_ready():

            self.log(

                "Backend sudah READY."

            )

            return True

        if not self.backend_file_exists():

            self.log(

                "ERROR: app.py tidak ditemukan."

            )

            return False

        self.log(

            "Memulai Backend app.py."

        )

        try:

            creationflags = 0

            if os.name == "nt":

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

        except Exception as err:

            self.log(

                f"Gagal menjalankan Backend: {err}"

            )

            return False

        self.log(

            "Menunggu backend pada "

            f"{self.BACKEND_HOST}:"

            f"{self.BACKEND_PORT}..."

        )

        timeout = 60

        start_time = time.time()

        while (

            time.time()

            -

            start_time

            <

            timeout

        ):

            if self.is_backend_ready():

                self.log(

                    "Backend READY."

                )

                self.log(

                    "Backend benar-benar READY."

                )

                return True

            if (

                self.backend_process

                and

                self.backend_process.poll()

                is not None

            ):

                self.log(

                    "Backend berhenti sebelum READY."

                )

                return False

            time.sleep(1)

        self.log(

            "TIMEOUT: Backend tidak READY."

        )

        return False

    # =====================================================
    # START BOT
    # =====================================================

    def start_bot(self):

        existing_pids = self.get_bot_pids()

        if existing_pids:

            self.log(

                "WhatsApp Bot sudah berjalan."

            )

            return True

        if not self.bot_file_exists():

            self.log(

                "ERROR: index.js tidak ditemukan."

            )

            self.log(

                f"Path: {self.bot_file}"

            )

            return False

        if not self.is_backend_ready():

            self.log(

                "Backend belum READY."

            )

            return False

        self.log(

            "Memulai WhatsApp Bot."

        )

        try:

            creationflags = 0

            if os.name == "nt":

                creationflags = (

                    subprocess.CREATE_NEW_PROCESS_GROUP

                )

            self.bot_process = subprocess.Popen(

                [

                    "node",

                    self.bot_file

                ],

                cwd=self.bot_dir,

                creationflags=creationflags

            )

            self.log(

                "Proses WhatsApp Bot berhasil dibuat."

            )

            time.sleep(3)

            if self.get_bot_pids():

                return True

            self.log(

                "WhatsApp Bot gagal berjalan."

            )

            return False

        except Exception as err:

            self.log(

                f"Gagal menjalankan Bot: {err}"

            )

            return False

    # =====================================================
    # START SYSTEM
    # =====================================================

    def start_system(self):

        if not self.control_lock.acquire(

            blocking=False

        ):

            self.log(

                "Operasi lain sedang berjalan."

            )

            return False

        self.operation = "STARTING"

        self.state = self.STARTING

        try:

            self.log(

                "Memulai START SYSTEM."

            )

            if not self.start_backend():

                self.state = self.OFFLINE

                return False

            if not self.start_bot():

                self.state = self.BACKEND_ONLY

                return False

            self.state = self.ONLINE

            self.log(

                "START SYSTEM BERHASIL."

            )

            return True

        finally:

            self.operation = None

            self.control_lock.release()

    # =====================================================
    # STOP SYSTEM
    # =====================================================

    def stop_system(self):

        if not self.control_lock.acquire(

            blocking=False

        ):

            self.log(

                "Operasi lain sedang berjalan."

            )

            return False

        self.operation = "STOPPING"

        self.state = self.STOPPING

        try:

            self.log(

                "Memulai STOP SYSTEM."

            )

            result = self.stop_bot_process_tree()

            if result:

                self.state = self.BACKEND_ONLY

                self.log(

                    "STOP SYSTEM BERHASIL."

                )

                return True

            self.state = self.ONLINE

            return False

        finally:

            self.operation = None

            self.control_lock.release()

    # =====================================================
    # RESTART SYSTEM
    # =====================================================

    def restart_bot(self):

        if not self.control_lock.acquire(

            blocking=False

        ):

            self.log(

                "Operasi lain sedang berjalan."

            )

            return False

        self.operation = "RESTARTING"

        self.state = self.RESTARTING

        try:

            self.log(

                "Memulai RESTART SYSTEM."

            )

            if not self.is_backend_ready():

                self.log(

                    "Backend belum READY."

                )

                self.state = self.OFFLINE

                return False

            if not self.stop_bot_process_tree():

                self.state = self.BACKEND_ONLY

                return False

            time.sleep(2)

            if not self.start_bot():

                self.state = self.BACKEND_ONLY

                return False

            self.state = self.ONLINE

            self.log(

                "RESTART SYSTEM BERHASIL."

            )

            return True

        finally:

            self.operation = None

            self.control_lock.release()

    # =====================================================
    # CHECK SYSTEM
    # =====================================================

    def check_system(self):

        self.log(

            "Memulai CHECK SYSTEM."

        )

        backend_process = (

            self.is_backend_process_running()

        )

        backend_port = (

            self.is_backend_port_open()

        )

        backend_ready = (

            self.is_backend_ready()

        )

        bot_pids = self.get_bot_pids()

        bot_process = bool(

            bot_pids

        )

        internet_available = self.is_internet_available()

        backend_file = (

            self.backend_file_exists()

        )

        bot_file = (

            self.bot_file_exists()

        )

        state_before_check = self.state

        if (

            backend_port

            and

            backend_ready

            and

            bot_process

            and

            internet_available

        ):

            system = self.ONLINE

        elif (

            backend_port

            and

            backend_ready

            and

            bot_process

            and

            not internet_available

        ):

            system =self.INTERNET_OFFLINE

        elif (

            backend_port

            and

            backend_ready

            and

            not bot_process

        ):

            system = self.BACKEND_ONLY

        elif (

            not backend_port

            and

            not bot_process

        ):

            system = self.OFFLINE

        else:

            system = "DEGRADED"

        self.state = system

        self.log(

            "CHECK SYSTEM selesai."

        )

        return {

            "backend_process":

                backend_process,

            "backend_port":

                backend_port,

            "backend_ready":

                backend_ready,

            "bot_process":

                bot_process,

            "bot_pids":

                bot_pids,

            "backend_file":

                backend_file,

            "bot_file":

                bot_file,

            "internet_available":

                internet_available,
            "state_before_check":

                state_before_check,

            "system":

                system

        }

    # =====================================================
    # STOP BACKEND
    # =====================================================

    def stop_backend(self):

        self.log("Memeriksa Backend pada port 5000.")

        # -------------------------------------------------
        # JIKA BACKEND SUDAH MATI
        # -------------------------------------------------

        if not self.is_backend_port_open():

            self.backend_process = None

            self.log(

                "Backend sudah tidak berjalan."

            )

            return True

        # -------------------------------------------------
        # CARI PID BACKEND BERDASARKAN PORT
        # -------------------------------------------------

        backend_pid = None

        try:

            result = subprocess.run(

                [

                    "netstat",

                    "-ano"

                ],

                capture_output=True,

                text=True,

                encoding="utf-8",

                errors="ignore"

            )

            for line in result.stdout.splitlines():

                parts = line.split()

                if len(parts) < 5:

                    continue

                if (

                    parts[0] == "TCP"

                    and

                    parts[1] == "127.0.0.1:5000"

                    and

                    parts[3] == "LISTENING"

                ):

                    backend_pid = int(

                        parts[4]

                    )

                    break

        except Exception as err:

            self.log(

                f"Gagal membaca PID Backend: {err}"

            )

            return False

        if not backend_pid:

            self.log(

                "PID Backend tidak ditemukan."

            )

            return False

        self.log(

            f"PID Backend ditemukan: {backend_pid}"

        )

        # -------------------------------------------------
        # HENTIKAN HANYA PID BACKEND TERATAI
        # -------------------------------------------------

        try:

            result = subprocess.run(

                [

                    "taskkill",

                    "/PID",

                    str(backend_pid),

                    "/T",

                    "/F"

                ],

                capture_output=True,

                text=True,

                encoding="utf-8",

                errors="ignore"

            )

            if result.returncode != 0:

                self.log(

                    "taskkill memberikan peringatan."

                )

        except Exception as err:

            self.log(

                f"Gagal menghentikan Backend: {err}"

            )

            return False

        # -------------------------------------------------
        # VALIDASI AKHIR
        # -------------------------------------------------

        timeout = 30

        start_time = time.time()

        while (

            time.time() - start_time < timeout

        ):

            if not self.is_backend_port_open():

                self.backend_process = None

                self.log(

                    "Backend berhasil dihentikan."

                )

                return True

            time.sleep(1)

        self.log(

            "Timeout menunggu port Backend berhenti."

        )

        return False

    # =====================================================
    # CLEAN CACHE
    # =====================================================

    def clean_cache(self):

        if not self.control_lock.acquire(
            blocking=False
        ):

            self.log(
                "Operasi lain sedang berjalan."
            )

            return False

        self.operation = "CLEAN_CACHE"

        try:

            self.log(
                "Memulai CLEAN CACHE."
            )

            # ---------------------------------------------
            # FOLDER YANG AMAN DIBERSIHKAN
            # ---------------------------------------------

            cache_directories = [

                os.path.join(
                    self.base_dir,
                    "backend",
                    "__pycache__"
                ),

                os.path.join(
                    self.base_dir,
                    "launcher",
                    "__pycache__"
                ),

                os.path.join(
                    self.base_dir,
                    "services",
                    "__pycache__"
                )

            ]

            removed_count = 0

            # ---------------------------------------------
            # HAPUS CACHE
            # ---------------------------------------------

            for cache_dir in cache_directories:

                if not os.path.exists(
                    cache_dir
                ):

                    continue

                try:

                    import shutil

                    shutil.rmtree(
                        cache_dir
                    )

                    removed_count += 1

                    self.log(
                        "Cache dibersihkan: "
                        + cache_dir
                    )

                except Exception as error:

                    self.log(
                        "Gagal membersihkan cache: "
                        + cache_dir
                        + " - "
                        + str(error)
                    )

            # ---------------------------------------------
            # HASIL
            # ---------------------------------------------

            self.log(
                "CLEAN CACHE selesai. "
                "Folder dibersihkan: "
                + str(
                    removed_count
                )
            )

            return True

        except Exception as error:

            self.log(
                "CLEAN CACHE gagal: "
                + str(error)
            )

            return False

        finally:

            self.operation = None

            self.control_lock.release()


    # =====================================================
    # SHUTDOWN SYSTEM
    # =====================================================

    def shutdown_system(self):

        if not self.control_lock.acquire(

            blocking=False

        ):

            self.log(

                "Operasi lain sedang berjalan."

            )

            return False

        self.operation = "SHUTDOWN"

        self.state = self.CLOSING

        try:

            self.log(

                "Memulai SHUTDOWN SYSTEM."

            )

            if not self.stop_bot_process_tree():

                return False

            if not self.stop_backend():

                return False

            self.backend_process = None

            self.bot_process = None

            self.state = self.OFFLINE

            self.log(

                "SHUTDOWN SYSTEM BERHASIL."

            )

            return True

        finally:

            self.operation = None

            self.control_lock.release()

    # =====================================================
    # CLOSE SYSTEM
    # =====================================================

    def close_system(self):

        if not self.control_lock.acquire(

            blocking=False

        ):

            self.log(

                "Operasi lain sedang berjalan."

            )

            return False

        self.operation = "CLOSING"

        self.state = self.CLOSING

        try:

            self.log(

                "Memulai CLOSE SYSTEM."

            )

            # ---------------------------------------------
            # STOP BOT
            # ---------------------------------------------

            bot_result = (

                self.stop_bot_process_tree()

            )

            if not bot_result:

                self.log(

                    "Peringatan: Bot tidak berhasil "

                    "dikonfirmasi berhenti."

                )

            # ---------------------------------------------
            # STOP BACKEND
            # ---------------------------------------------

            backend_result = (

                self.stop_backend()

            )

            if not backend_result:

                self.log(

                    "Peringatan: Backend tidak berhasil "

                    "dikonfirmasi berhenti."

                )

            # ---------------------------------------------
            # VALIDASI AKHIR
            # ---------------------------------------------

            bot_still_running = bool(

                self.get_bot_pids()

            )

            backend_still_running = (

                self.is_backend_port_open()

            )

            if (

                not bot_still_running

                and

                not backend_still_running

            ):

                self.backend_process = None

                self.bot_process = None

                self.state = self.OFFLINE

                self.log(

                    "CLOSE SYSTEM BERHASIL."

                )

                return True

            self.log(

                "CLOSE SYSTEM selesai dengan peringatan."

            )

            return False

        finally:

            self.operation = None

            self.control_lock.release()



# =====================================================
# SINGLETON
# =====================================================

system_controller = SystemController()