from services.system_controller import system_controller


print("=" * 60)
print("TEST RESTART SYSTEM")
print("=" * 60)


result = system_controller.restart_bot()


print()
print("=" * 60)
print("HASIL RESTART SYSTEM")
print("=" * 60)


print(
    "HASIL RESTART :",
    result
)


print(
    "STATE         :",
    system_controller.state
)


print("=" * 60)