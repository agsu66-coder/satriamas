from services.excel_service import excel_service


class ConfigService:

    def __init__(self):
        self.config = {}
        self.reload()

    # =========================

    def reload(self):

        rows = excel_service.read_rows("KONFIGURASI")

        self.config = {}

        for row in rows[1:]:

            if len(row) < 2:
                continue

            key = row[0]
            value = row[1]

            if key:
                self.config[str(key).strip()] = value

    # =========================

    def get(self, key, default=None):

        return self.config.get(key, default)

    # =========================

    def get_int(self, key, default=0):

        try:
            return int(self.get(key))
        except:
            return default

    # =========================

    def get_float(self, key, default=0.0):

        try:
            return float(self.get(key))
        except:
            return default

    # =========================

    def get_bool(self, key, default=False):

        value = str(self.get(key)).lower()

        return value in [
            "true",
            "1",
            "yes",
            "ya"
        ]


config_service = ConfigService()