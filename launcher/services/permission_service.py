class PermissionService:

    # ==========================================
    # DAFTAR HAK AKSES
    # ==========================================

    PERMISSIONS = {

        "USER": {

            "VIEW_DASHBOARD",
            "CHECK_SYSTEM",
            "VIEW_LOG",
            "VIEW_REPORT"

        },

        "ADMIN": {

            "VIEW_DASHBOARD",
            "CHECK_SYSTEM",
            "VIEW_LOG",
            "VIEW_REPORT",

            "START_SYSTEM",
            "STOP_SYSTEM",
            "RESTART_SYSTEM",
            "CLEAN_CACHE",

            "EDIT_BRANDING",
            "EDIT_THEME"

        },

        "SUPERADMIN": {

            "VIEW_DASHBOARD",
            "CHECK_SYSTEM",
            "VIEW_LOG",
            "VIEW_REPORT",

            "START_SYSTEM",
            "STOP_SYSTEM",
            "RESTART_SYSTEM",
            "CLEAN_CACHE",

            "EDIT_BRANDING",
            "EDIT_THEME",

            "MANAGE_USERS",
            "SYSTEM_CONFIGURATION",
            "BACKUP_SYSTEM",
            "RESTORE_SYSTEM"

        }

    }

    # ==========================================
    # CEK HAK AKSES
    # ==========================================

    @classmethod
    def can(cls, role, action):

        if not role or not action:

            return False

        role = str(role).upper()
        action = str(action).upper()

        permissions = cls.PERMISSIONS.get(role)

        if not permissions:

            return False

        return action in permissions

    # ==========================================
    # AMBIL SEMUA HAK AKSES ROLE
    # ==========================================

    @classmethod
    def get_permissions(cls, role):

        role = str(role).upper()

        return cls.PERMISSIONS.get(

            role,

            set()

        )

    # ==========================================
    # CEK ROLE VALID
    # ==========================================

    @classmethod
    def is_valid_role(cls, role):

        if not role:

            return False

        return str(role).upper() in cls.PERMISSIONS


permission_service = PermissionService()