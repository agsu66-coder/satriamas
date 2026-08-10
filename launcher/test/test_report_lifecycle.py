import os
import sys

from datetime import date


# ==========================================================
# ROOT PATH
# ==========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


LAUNCHER_DIR = os.path.dirname(
    CURRENT_DIR
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



# ==========================================================
# HEADER
# ==========================================================

print("\n========================================")
print("     TEST REPORT LIFECYCLE TERATAI AI")
print("========================================\n")



# ==========================================================
# STEP 1
# REPORT PERIOD
# ==========================================================

print("[1] Menentukan periode laporan...")


tanggal_mulai = date(
    2026,
    7,
    1
)


tanggal_akhir = date(
    2026,
    7,
    31
)


print(
    "Periode:",
    tanggal_mulai,
    "-",
    tanggal_akhir
)



# ==========================================================
# STEP 2
# LOAD REPORT DATA
# ==========================================================

print("\n[2] Mengambil data laporan...")


summary = report_service.get_summary(

    tanggal_mulai,

    tanggal_akhir

)


print(
    "Report summary berhasil dibuat."
)


print(summary)



# ==========================================================
# STEP 3
# VALIDASI DATA
# ==========================================================

print("\n[3] Validasi struktur laporan...")


required_section = [

    "periode",

    "aktivitas",

    "aduan"

]


for item in required_section:


    if item not in summary:

        raise Exception(

            f"Section laporan tidak ditemukan: {item}"

        )


print(
    "Struktur laporan OK."
)



# ==========================================================
# STEP 4
# GENERATE PDF
# ==========================================================

print("\n[4] Membuat file PDF...")


REPORT_FOLDER = os.path.join(

    LAUNCHER_DIR,

    "reports",

    "test"

)


os.makedirs(

    REPORT_FOLDER,

    exist_ok=True

)


pdf_file = os.path.join(

    REPORT_FOLDER,

    "Laporan_TERATAI_Test.pdf"

)



report_pdf_service.generate_pdf(

    summary,

    pdf_file

)



print(
    "PDF dibuat:"
)

print(
    pdf_file
)



# ==========================================================
# STEP 5
# VALIDASI FILE
# ==========================================================

print("\n[5] Memeriksa file PDF...")


if not os.path.exists(pdf_file):

    raise Exception(

        "File PDF tidak ditemukan."

    )


file_size = os.path.getsize(

    pdf_file

)


if file_size == 0:

    raise Exception(

        "File PDF kosong."

    )


print(
    "Ukuran PDF:",
    file_size,
    "bytes"
)


print(
    "Validasi PDF OK."
)



# ==========================================================
# RESULT
# ==========================================================

print("\n========================================")
print(" TEST REPORT LIFECYCLE BERHASIL")
print("========================================\n")