from services.excel_service import excel_service

print("=" * 40)

print("TEST EXCEL ENGINE")

print("=" * 40)

excel_service.load_workbook()

print("Workbook OK")

print()

print("Sheet FAQ :", excel_service.sheet_exists("FAQ"))

print("Sheet TEMPLATE :", excel_service.sheet_exists("TEMPLATE"))

print()

print("Header TEMPLATE")

print(excel_service.headers("TEMPLATE"))

print()

print("Jumlah Template")

print(len(excel_service.read_sheet("TEMPLATE")))

print()

print("Cari WELCOME")

print(
    excel_service.find(
        "TEMPLATE",
        "KEY",
        "WELCOME"
    )
)

print()

print("Validation")

excel_service.validate_sheet(
    "TEMPLATE",
    [
        "KEY",
        "Kategori",
        "Isi_Pesan"
    ]
)

print("VALID")