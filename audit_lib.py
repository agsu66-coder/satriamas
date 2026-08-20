import os
import re

imports = set()
project_dir = r"E:\Teratai Proyek\v0.2"

# Pola untuk mendeteksi perintah import di Python
import_pattern = re.compile(r"^\s*(?:import\s+(\w+)|from\s+(\w+)\s+import)")

for root, dirs, files in os.walk(project_dir):
    # Lewati folder venv, git, dan node_modules
    if ".git" in root or "node_modules" in root or "venv" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = import_pattern.match(line)
                        if match:
                            lib = match.group(1) or match.group(2)
                            if lib:
                                imports.add(lib)
            except Exception:
                pass

print("=== DAFTAR LIBRARY YANG TERDETEKSI DIIMPOR DALAM KODE ===")
for lib in sorted(imports):
    print(lib)