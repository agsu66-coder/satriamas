from services.system_controller import system_controller


print("=" * 60)
print("TEST STOP SYSTEM")
print("=" * 60)


result = system_controller.stop_system()


print()
print("=" * 60)
print("HASIL STOP SYSTEM")
print("=" * 60)


print(
    "HASIL STOP :",
    result
)


print(
    "STATE      :",
    system_controller.state
)


print("=" * 60)