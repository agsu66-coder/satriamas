from services.excel_service import excel_service
from services.text_processor import text_processor
from services.knowledge_validator import KnowledgeValidator


class KnowledgeService:

    def __init__(self):

        self.sheet_name = "FAQ"

        self.records = []

        self.training_data = []

        self.statistics_data = {}

        self.audit_results = []

        self.validator = KnowledgeValidator()
    # ===========================================

    def load(self):
        """
        Membaca seluruh FAQ kemudian
        membangun training data.
        """

        self.records.clear()
        self.training_data.clear()
        self.audit_results.clear()

        rows = excel_service.read_as_dict(
            self.sheet_name
        )

        total = 0
        active = 0
        inactive = 0

        for row in rows:

            total += 1

            self.records.append(row)

            audit = self.validator.validate(
                row
            )

            self.audit_results.append(
                audit
            )

            status = str(
                row.get("Status", "")
            ).strip().upper()

            if status != "AKTIF":

                inactive += 1

                continue

            active += 1

            text_parts = []

            # ==========================
            # Kategori
            # ==========================

            kategori = str(
                row.get("Kategori", "")
            ).strip()

            if kategori:
                text_parts.append(kategori)

            # ==========================
            # Keyword
            # ==========================

            keyword = str(
                row.get("Keyword", "")
            ).strip()

            if keyword:

                for item in keyword.split(";"):

                    item = item.strip()

                    if item:
                        text_parts.append(item)

            # ==========================
            # Variasi Dinamis
            # ==========================

            for column, value in row.items():

                if not column.startswith("Variasi_"):
                    continue

                value = str(value).strip()

                if value:
                    text_parts.append(value)

            # ==========================
            # Normalisasi
            # ==========================

            training_text = text_processor.normalize(
                " ".join(text_parts)
            )

            self.training_data.append({

                "key":
                    row.get("ID", ""),

                "category":
                    kategori,

                "text":
                    training_text,

                "answer":
                    row.get("Jawaban", "")

            })

        self.statistics_data = {

            "total":
                total,

            "active":
                active,

            "inactive":
                inactive,

            "training":
                len(self.training_data)

        }

        return True

    # ===========================================

    def reload(self):

        excel_service.reload_workbook()

        return self.load()

    # ===========================================

    def statistics(self):

        return self.statistics_data

    # ===========================================

    def total(self):

        return len(
            self.records
        )

    # ===========================================

    def get_all(self):

        return self.records

    # ===========================================

    def get_records(self):
        """
        Mengembalikan seluruh record FAQ
        yang telah dimuat ke memory.
        Digunakan oleh KnowledgeEngine.
        """

        return self.records

    # ===========================================

    def get_training_data(self):

        return self.training_data

    # ===========================================

    def exists(self, key):

        key = str(key).strip()

        for row in self.records:

            if str(row.get("ID", "")).strip() == key:

                return True

        return False

    # ===========================================

    def find_by_key(self, key):

        key = str(key).strip()

        for row in self.records:

            if str(row.get("ID", "")).strip() == key:

                return row

        return None

    def get_audit_results(self):

        return self.audit_results

knowledge_service = KnowledgeService()