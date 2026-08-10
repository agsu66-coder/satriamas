from services.system_controller import system_controller

import time


print("=" * 60)
print("TEST CHECK SYSTEM - ONLINE")
print("=" * 60)


print()
print("MEMULAI SISTEM...")
print()


hasil_start = system_controller.start_system()


print()
print("HASIL START SYSTEM")
print("==================")

print(
    "HASIL START :",
    hasil_start
)

print(
    "STATE       :",
    system_controller.get_state()
)


print()
print("=" * 60)
print("MENUNGGU 10 DETIK")
print("=" * 60)


time.sleep(10)


print()
print("=" * 60)
print("MENJALANKAN CHECK SYSTEM")
print("=" * 60)


hasil_check = system_controller.check_system()


print()


for key, value in hasil_check.items():

    print(

        f"{key:25} : {value}"

    )


print()
print("=" * 60)
print("HASIL AKHIR")
print("=" * 60)


if hasil_check.get("system") == "ONLINE":

    print(
        "CHECK SYSTEM : ONLINE"
    )

else:

    print(
        "CHECK SYSTEM : TIDAK ONLINE"
    )