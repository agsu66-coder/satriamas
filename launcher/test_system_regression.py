import sys
import time

from system_controller import system_controller


def print_result(title, result):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

    for key, value in result.items():

        print(
            f"{key:<24}: {value}"
        )


def check_status(expected):

    result = system_controller.check_system()

    print_result(
        "HASIL CHECK SYSTEM",
        result
    )

    actual = result["system"]

    if actual == expected:

        print(
            f"\nPASS: Status sesuai -> {expected}"
        )

        return True

    print(
        f"\nFAIL: Status tidak sesuai."
    )

    print(
        f"Expected: {expected}"
    )

    print(
        f"Actual  : {actual}"
    )

    return False


def main():

    print("=" * 60)
    print("TERATAI AI - SYSTEM REGRESSION TEST")
    print("=" * 60)

    # -------------------------------------------------
    # 1. CHECK KONDISI AWAL
    # -------------------------------------------------

    print()
    print("TAHAP 1: CHECK KONDISI AWAL")

    initial = system_controller.check_system()

    print_result(
        "KONDISI AWAL",
        initial
    )

    # -------------------------------------------------
    # 2. START SYSTEM
    # -------------------------------------------------

    print()
    print("TAHAP 2: START SYSTEM")

    if not system_controller.start_system():

        print(
            "\nFAIL: START SYSTEM gagal."
        )

        return False

    if not check_status(

        system_controller.ONLINE

    ):

        return False

    # -------------------------------------------------
    # 3. RESTART BOT
    # -------------------------------------------------

    print()
    print("TAHAP 3: RESTART BOT")

    if not system_controller.restart_bot():

        print(
            "\nFAIL: RESTART BOT gagal."
        )

        return False

    if not check_status(

        system_controller.ONLINE

    ):

        return False

    # -------------------------------------------------
    # 4. STOP BOT
    # -------------------------------------------------

    print()
    print("TAHAP 4: STOP SYSTEM")

    if not system_controller.stop_system():

        print(
            "\nFAIL: STOP SYSTEM gagal."
        )

        return False

    if not check_status(

        system_controller.BACKEND_ONLY

    ):

        return False

    # -------------------------------------------------
    # 5. START KEMBALI
    # -------------------------------------------------

    print()
    print("TAHAP 5: START KEMBALI")

    if not system_controller.start_system():

        print(
            "\nFAIL: START SYSTEM kedua gagal."
        )

        return False

    if not check_status(

        system_controller.ONLINE

    ):

        return False

    # -------------------------------------------------
    # 6. SHUTDOWN PENUH
    # -------------------------------------------------

    print()
    print("TAHAP 6: SHUTDOWN SYSTEM")

    if not system_controller.shutdown_system():

        print(
            "\nFAIL: SHUTDOWN SYSTEM gagal."
        )

        return False

    if not check_status(

        system_controller.OFFLINE

    ):

        return False

    print()
    print("=" * 60)
    print("REGRESSION TEST BERHASIL")
    print("=" * 60)

    return True


if __name__ == "__main__":

    success = main()

    if success:

        sys.exit(0)

    sys.exit(1)