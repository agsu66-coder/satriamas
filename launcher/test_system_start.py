import os
from services.system_controller import system_controller


print("=" * 60)
print("TEST START SYSTEM")
print("=" * 60)


print()
print("PEMERIKSAAN LOKASI FILE")
print("=======================")


project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


print(
    "PROJECT ROOT :",
    project_root
)


backend_file = os.path.join(
    project_root,
    "backend",
    "app.py"
)


bot_file = os.path.join(
    project_root,
    "bot",
    "index.js"
)


print(
    "BACKEND FILE :",
    backend_file
)


print(
    "BACKEND ADA  :",
    os.path.exists(backend_file)
)


print(
    "BOT FILE     :",
    bot_file
)


print(
    "BOT ADA      :",
    os.path.exists(bot_file)
)


print()
print("=" * 60)
print("MEMULAI START SYSTEM")
print("=" * 60)


result = system_controller.start_system()


print()
print("=" * 60)
print("HASIL START SYSTEM")
print("=" * 60)


print(
    "HASIL START :",
    result
)


print(
    "STATE       :",
    system_controller.state
)


print("=" * 60)