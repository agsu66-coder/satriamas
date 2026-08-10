from services.system_controller import system_controller

import time


print("=" * 60)

print("TEST START / STOP SYSTEM TERATAI AI")

print("=" * 60)


# ==========================================
# CHECK SYSTEM
# ==========================================

print("\n1. CHECK SYSTEM")

check = system_controller.check_system()

print(check)


if not check["success"]:

    print(

        "\n❌ SISTEM BELUM SIAP."

    )

    exit()


# ==========================================
# START SYSTEM
# ==========================================

print("\n2. START SYSTEM")

start_result = (

    system_controller.start_system()

)

print(

    "HASIL START :",

    start_result

)


time.sleep(5)


# ==========================================
# CEK STATUS
# ==========================================

print("\n3. STATUS SETELAH START")

status = (

    system_controller.get_status()

)

print(status)


# ==========================================
# STOP SYSTEM
# ==========================================

print("\n4. STOP SYSTEM")

stop_result = (

    system_controller.stop_system()

)

print(

    "HASIL STOP :",

    stop_result

)


# ==========================================
# STATUS AKHIR
# ==========================================

print("\n5. STATUS AKHIR")

status = (

    system_controller.get_status()

)

print(status)


print("\n")

print("=" * 60)

print("TEST SELESAI")

print("=" * 60)