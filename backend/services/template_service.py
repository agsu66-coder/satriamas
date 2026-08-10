from services.excel_service import excel_service


class TemplateService:

    def __init__(self):

        self.sheet_name = "TEMPLATE"

        self.templates = {}

        self.load_templates()


    # =====================================
    # LOAD TEMPLATE
    # =====================================

    def load_templates(self):

        rows = excel_service.read_as_dict(

            self.sheet_name

        )

        self.templates = {}

        for row in rows:

            key = row.get("KEY")

            if not key:

                continue

            row["Isi_Pesan"] = self.clean_text(
                row.get("Isi_Pesan")
            )

            self.templates[

                str(key).strip().upper()

            ] = row


    # =====================================
    # MEMBERSIHKAN FORMAT EXCEL
    # =====================================

    def clean_text(self, text):

        if not text:

            return ""

        text = (
            str(text)
            .replace("_x000D_", "\n")
            .replace("\\n", "\n")
            .replace("\r\n", "\n")
            .replace("\r", "\n")
        )

        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")

        return text.strip()

    # =====================================
    # AMBIL TEMPLATE
    # =====================================

    def get(self, key):

        if not key:

            return None

        key = str(key).strip().upper()

        template = self.templates.get(key)

        if not template:

            return None

        return template.get("Isi_Pesan")


    # =====================================
    # RENDER TEMPLATE
    # =====================================

    def render(self, key, variables=None):

        message = self.get(key)

        if not message:

            return None

        if not variables:

            return message

        for variable, value in variables.items():

            placeholder = "{" + variable + "}"

            message = message.replace(

                placeholder,

                str(value)

            )

        return message


template_service = TemplateService()