from services.system_controller import system_controller

import time


print("=" * 60)
print("TEST START SYSTEM")
print("=" * 60)


hasil = system_controller.start_system()


print()
print("=" * 60)
print("HASIL START SYSTEM")
print("=" * 60)


print(
    "HASIL START :",
    hasil
)


print(
    "STATE       :",
    system_controller.get_state()
)


print()
print("=" * 60)
print("MENUNGGU 10 DETIK UNTUK STABILISASI")
print("=" * 60)


time.sleep(10)


print()
print("=" * 60)
print("CHECK SYSTEM SETELAH START")
print("=" * 60)


hasil_check = system_controller.check_system()


for key, value in hasil_check.items():

    print(

        f"{key:25} : {value}"

    )


print()
print("=" * 60)
print("TEST SELESAI")
print("=" * 60)