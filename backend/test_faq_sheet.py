from services.excel_service import excel_service

print("=" * 40)
print("TEST FAQ SHEET")
print("=" * 40)

print("\nDaftar Sheet")
print(excel_service.get_sheet_names())

print("\nJumlah Baris FAQ")

rows = excel_service.read_rows("FAQ")

print(len(rows))

print("\n5 Baris Pertama")

for i, row in enumerate(rows[:5], start=1):
    print(f"{i}. {row}")

print("=" * 40)