from services.system_controller import system_controller

import time


print("=" * 60)

print("TEST SYSTEM LIFECYCLE TERATAI AI")

print("=" * 60)


# ==================================================
# CHECK SYSTEM
# ==================================================

print("\n1. CHECK SYSTEM")

check = (

    system_controller.check_system()

)

print(check)


if not check["success"]:

    print(

        "\nSISTEM TIDAK SIAP."

    )

    exit()


# ==================================================
# START SYSTEM
# ==================================================

print("\n2. START SYSTEM")

start_result = (

    system_controller.start_system()

)

print(

    "HASIL START :",

    start_result

)


if not start_result:

    print(

        "\nSTART SYSTEM GAGAL."

    )

    exit()


# ==================================================
# STATUS AFTER START
# ==================================================

print("\n3. STATUS AFTER START")

print(

    system_controller.get_status()

)


print(

    "\nSistem berjalan selama 30 detik."

)

time.sleep(

    30

)


# ==================================================
# STOP SYSTEM
# ==================================================

print("\n4. STOP SYSTEM")

stop_result = (

    system_controller.stop_system()

)

print(

    "HASIL STOP :",

    stop_result

)


# ==================================================
# STATUS AFTER STOP
# ==================================================

print("\n5. STATUS AFTER STOP")

print(

    system_controller.get_status()

)


print("\n")

print("=" * 60)

print("TEST LIFECYCLE SELESAI")

print("=" * 60)