from services.template_service import template_service

print("=" * 40)
print("TEST TEMPLATE ENGINE")
print("=" * 40)

# ---------------------------------
print("\nLoad Template")

template_service.load()

print("OK")

# ---------------------------------
print("\nJumlah Template")

print(len(template_service.get_all_keys()))

# ---------------------------------
print("\nDaftar KEY")

for key in template_service.get_all_keys():

    print("-", key)

# ---------------------------------
print("\nCari Template")

print(
    template_service.get_message(
        "WELCOME"
    )
)

# ---------------------------------
print("\nPlaceholder")

print(

    template_service.get_message(

        "WELCOME",

        nama="Administrator"

    )

)

# ---------------------------------
print("\nExists")

print(

    template_service.exists(

        "WELCOME"

    )

)

print(

    template_service.exists(

        "ABCXYZ"

    )

)

# ---------------------------------
print("\nReload")

template_service.reload()

print("Reload OK")

print("=" * 40)