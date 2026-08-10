"""
==================================================
TERATAI AI
Global Constants
==================================================

Module  : constants
Version : 1.0.0
Status  : DEVELOPMENT (Tahap Migrasi)

Single Source of Truth untuk seluruh konstanta
yang digunakan oleh TERATAI.

Setelah seluruh proses migrasi selesai dan
seluruh pengujian dinyatakan PASS,
status file ini akan berubah menjadi LOCK.

==================================================
"""

# ======================================================
# SYSTEM
# ======================================================

SYSTEM_NAME = "TERATAI AI"

SYSTEM_VERSION = "0.3.0"
# ======================================================
# AI MODEL
# ======================================================

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# ======================================================
# WORKBOOK
# ======================================================

WORKBOOK_NAME = "TERATAI_CORE.xlsx"

# ======================================================
# SHEET
# ======================================================

SHEET_FAQ = "FAQ"

SHEET_TEMPLATE = "TEMPLATE"

SHEET_PETUGAS = "PETUGAS"

SHEET_PENGADUAN = "PENGADUAN"

SHEET_KONFIGURASI = "KONFIGURASI"

SHEET_LOG = "LOG"

SHEET_DASHBOARD = "DASHBOARD"

SHEET_MASTER_KATEGORI = "MASTER_KATEGORI"

SHEET_VERSI = "VERSI"

SHEET_CHANGELOG = "CHANGELOG"

# ======================================================
# STATUS
# ======================================================

STATUS_ACTIVE = "AKTIF"

STATUS_INACTIVE = "NONAKTIF"

# ======================================================
# FAQ COLUMN
# Mengikuti struktur workbook TERATAI_CORE.xlsx
# ======================================================

COL_ID = "ID"

COL_CATEGORY = "Kategori"

COL_KEYWORD = "Keyword"

COL_ANSWER = "Jawaban"

COL_SOURCE = "Sumber"

COL_STATUS = "Status"

COL_LAST_UPDATE = "Terakhir_Update"

VARIATION_PREFIX = "Variasi_"

# ======================================================
# TEMPLATE COLUMN
# ======================================================

COL_TEMPLATE_KEY = "KEY"

COL_TEMPLATE_MESSAGE = "Isi_Pesan"

# ======================================================
# CONFIG COLUMN
# ======================================================

COL_CONFIG_KEY = "KEY"

COL_CONFIG_VALUE = "VALUE"

# ======================================================
# MATCH METHOD
# ======================================================

MATCH_EXACT = "exact"

MATCH_KEYWORD = "keyword"

MATCH_SEMANTIC = "semantic"

MATCH_NOT_FOUND = "not_found"

# ======================================================
# DEFAULT VALUE
# ======================================================

DEFAULT_CATEGORY = "Umum"

DEFAULT_SCORE = 0.0

DEFAULT_THRESHOLD = 0.75

# ======================================================
# SEMANTIC
# ======================================================

SEMANTIC_THRESHOLD = 0.50

# ======================================================
# SEARCH THRESHOLD
# ======================================================

MIN_KEYWORD_SCORE = 3

SEMANTIC_THRESHOLD = 0.45