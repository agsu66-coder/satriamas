from services.auth_service import auth_service
from services.permission_service import permission_service


print("=" * 60)
print("TEST AUTH CORE TERATAI AI")
print("=" * 60)


# ==========================================
# TEST LOGIN USER
# ==========================================

result = auth_service.login(

    "operator",

    "operator123"

)

print("\nLOGIN USER")

print(result)


# ==========================================
# TEST LOGIN ADMIN
# ==========================================

result = auth_service.login(

    "admin",

    "admin123"

)

print("\nLOGIN ADMIN")

print(result)


# ==========================================
# TEST LOGIN SUPERADMIN
# ==========================================

result = auth_service.login(

    "superadmin",

    "superadmin123"

)

print("\nLOGIN SUPERADMIN")

print(result)


# ==========================================
# TEST PERMISSION
# ==========================================

print("\nPERMISSION TEST")


tests = [

    ("USER", "VIEW_DASHBOARD"),

    ("USER", "CLEAN_CACHE"),

    ("ADMIN", "CLEAN_CACHE"),

    ("ADMIN", "MANAGE_USERS"),

    ("SUPERADMIN", "MANAGE_USERS"),

    ("SUPERADMIN", "BACKUP_SYSTEM")

]


for role, action in tests:

    result = permission_service.can(

        role,

        action

    )

    print(

        f"{role:12} "

        f"{action:25} "

        f"{result}"

    )


print("\n")

print("=" * 60)
print("TEST SELESAI")
print("=" * 60)