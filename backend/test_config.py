from services.config_service import config_service

print("Nama Instansi :",
      config_service.get("NAMA_INSTANSI"))

print("Threshold :",
      config_service.get_float("THRESHOLD_AI"))

print("Port :",
      config_service.get_int("PORT_FLASK"))

print("Versi :",
      config_service.get("VERSI"))