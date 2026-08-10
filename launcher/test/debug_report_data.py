import sys
import os

from datetime import date

LAUNCHER_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(
    0,
    LAUNCHER_DIR
)

from services.report_service import report_service


workbook = report_service.load_workbook()


# ==========================================================
# DEBUG AKTIVITAS
# ==========================================================

print("\n========================================")
print("        DATA AKTIVITAS")
print("========================================\n")

aktivitas = report_service.read_sheet(
    workbook,
    "AKTIVITAS"
)

for nomor, item in enumerate(
    aktivitas,
    start=1
):

    print(
        f"{nomor}. "
        f"Waktu={item.get('Waktu')} | "
        f"Jenis={item.get('Jenis_Aktivitas')} | "
        f"User_Key={item.get('User_Key')} | "
        f"No_WA={item.get('No_WA')}"
    )


# ==========================================================
# DEBUG ADUAN
# ==========================================================

print("\n========================================")
print("        DATA ADUAN")
print("========================================\n")

aduan = report_service.read_sheet(
    workbook,
    "ADUAN"
)


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


total = 0


for nomor, item in enumerate(

    aduan,

    start=1

):

    tanggal = item.get(

        "Tanggal"

    )


    status = item.get(

        "Status"

    )


    if report_service.in_period(

        tanggal,

        tanggal_mulai,

        tanggal_akhir

    ):

        total += 1


        print(

            f"{nomor}. "

            f"ID={item.get('ID')} | "

            f"Tanggal={tanggal} | "

            f"Status={status}"

        )


print("\n========================================")

print(

    f"TOTAL ADUAN DALAM PERIODE: {total}"

)

print("========================================\n")