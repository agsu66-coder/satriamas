from services.system_controller import system_controller


print("=" * 60)
print("TEST CHECK SYSTEM")
print("=" * 60)


result = system_controller.check_system()


print()
print("HASIL CHECK SYSTEM")
print("==================")


print(
    "backend_process :",
    result.get("backend_process")
)


print(
    "backend_port    :",
    result.get("backend_port")
)


print(
    "backend_ready   :",
    result.get("backend_ready")
)


print(
    "bot_process     :",
    result.get("bot_process")
)


print(
    "backend_file    :",
    result.get("backend_file")
)


print(
    "bot_file        :",
    result.get("bot_file")
)


print(
    "state_before_check :",
    result.get("state_before_check")
)


print(
    "system             :",
    result.get("system")
)


print()
print("=" * 60)


system = result.get("system")


if system == "ONLINE":

    print(
        "CHECK SYSTEM : ONLINE"
    )


elif system == "BACKEND_ONLY":

    print(
        "CHECK SYSTEM : BACKEND ONLY"
    )


elif system == "OFFLINE":

    print(
        "CHECK SYSTEM : OFFLINE"
    )


else:

    print(
        "CHECK SYSTEM :",
        system
    )


print("=" * 60)