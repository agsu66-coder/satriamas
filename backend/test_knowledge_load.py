from services.excel_service import excel_service

print("Workbook :", excel_service.file_path)

rows = excel_service.read_rows("FAQ")

print("Jumlah baris :", len(rows))

for i, row in enumerate(rows[:5]):
    print(i, row)