import sys
import os

from datetime import date

# ==========================================================
# ROOT LAUNCHER
# ==========================================================

LAUNCHER_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    LAUNCHER_DIR
)

# ==========================================================
# IMPORT SERVICE
# ==========================================================

from services.report_service import report_service
from services.report_pdf_service import report_pdf_service

print("\n========================================")
print("      TEST REPORT SERVICE LAUNCHER")
print("========================================\n")

# ==========================================================
# AMBIL DATA LAPORAN
# ==========================================================

summary = report_service.get_summary(
    date(2026, 7, 1),
    date(2026, 7, 31)
)

print(summary)

# ==========================================================
# BUAT FOLDER REPORTS
# ==========================================================

reports_dir = os.path.join(
    LAUNCHER_DIR,
    "reports"
)

os.makedirs(
    reports_dir,
    exist_ok=True
)

pdf_file = os.path.join(
    reports_dir,
    "test_report.pdf"
)

# ==========================================================
# GENERATE PDF
# ==========================================================

report_pdf_service.generate_pdf(
    summary,
    pdf_file
)

print("\nPDF berhasil dibuat:")
print(pdf_file)

print("\n========================================")
print("        TEST SELESAI")
print("========================================\n")