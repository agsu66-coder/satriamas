class KnowledgeValidator:
    """
    Validator kualitas FAQ TERATAI.

    Input:
        dictionary dari ExcelService

    Output:
        hasil audit FAQ
    """

    def __init__(self):

        self.required_fields = [
            "ID",
            "Kategori",
            "Keyword",
            "Jawaban"
        ]


    # =======================================

    def validate(self, row):

        result = {

            "FAQ_ID":
                row.get("ID", ""),

            "Intent_Check":
                "PASS",

            "Keyword_Check":
                "PASS",

            "Variation_Check":
                "PASS",

            "Answer_Check":
                "PASS",

            "Quality_Score":
                100,

            "Risk_Level":
                "LOW",

            "Audit_Status":
                "PASS",

            "Errors": [],

            "Warnings": []

        }


        self.check_required(
            row,
            result
        )


        self.check_keyword(
            row,
            result
        )


        self.check_variations(
            row,
            result
        )


        self.check_answer(
            row,
            result
        )


        self.calculate_result(
            result
        )


        return result


    # =======================================

    def check_required(self, row, result):

        for field in self.required_fields:

            value = str(
                row.get(field, "")
            ).strip()


            if not value:

                result["Errors"].append(
                    f"{field} kosong"
                )


    # =======================================

    def check_keyword(self, row, result):

        keyword = str(
            row.get("Keyword", "")
        ).strip()


        if not keyword:

            result["Keyword_Check"] = "FAILED"

            result["Errors"].append(
                "Keyword kosong"
            )

            return


        keywords = [
            x.strip()
            for x in keyword.split(";")
            if x.strip()
        ]


        if len(keywords) == 1:

            result["Keyword_Check"] = "REVIEW"

            result["Warnings"].append(
                "Keyword hanya satu"
            )


    # =======================================

    def check_variations(self, row, result):

        variations = []


        for column, value in row.items():

            if column.startswith(
                "Variasi_"
            ):

                value = str(
                    value
                ).strip()


                if value:

                    variations.append(value)



        if len(variations) == 0:

            result["Variation_Check"] = "FAILED"

            result["Errors"].append(
                "Tidak ada variasi"
            )


        elif len(variations) < 3:

            result["Variation_Check"] = "REVIEW"

            result["Warnings"].append(
                "Variasi kurang dari 3"
            )


    # =======================================

    def check_answer(self, row, result):

        jawaban = str(
            row.get("Jawaban", "")
        ).strip()


        if not jawaban:

            result["Answer_Check"] = "FAILED"

            result["Errors"].append(
                "Jawaban kosong"
            )


    # =======================================

    def calculate_result(self, result):

        error_count = len(
            result["Errors"]
        )

        warning_count = len(
            result["Warnings"]
        )


        if error_count > 0:

            result["Audit_Status"] = "FAILED"

            result["Risk_Level"] = "HIGH"

            result["Quality_Score"] = 50


        elif warning_count > 0:

            result["Audit_Status"] = "REVIEW"

            result["Risk_Level"] = "MEDIUM"

            result["Quality_Score"] = 80