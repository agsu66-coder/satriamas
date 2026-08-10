from services.excel_service import excel_service
from services.text_processor import text_processor


class BoundaryService:

    def __init__(self):

        self.sheet_name = "BOUNDARY"

        self.rules = []

        self.loaded = False


    # ==========================================
    # LOAD BOUNDARY
    # ==========================================

    def load(self):

        self.rules.clear()

        rows = excel_service.read_as_dict(
            self.sheet_name
        )


        for row in rows:

            status = str(
                row.get("Status", "")
            ).strip().upper()


            if status != "AKTIF":
                continue


            self.rules.append({

                "id":
                    row.get("ID", ""),

                "faq_id":
                    row.get("FAQ_ID", ""),

                "intent":
                    row.get("Intent", ""),

                "positive":
                    self._parse_signal(
                        row.get("Positive_Signal", "")
                    ),

                "negative":
                    self._parse_signal(
                        row.get("Negative_Signal", "")
                    ),

                "priority":
                    row.get("Priority", "")

            })


        self.loaded = True

        return True



    # ==========================================
    # PARSE SIGNAL
    # ==========================================

    def _parse_signal(self, value):

        if not value:

            return []


        return [

            text_processor.normalize(
                item.strip()
            )

            for item in str(value).split(";")

            if item.strip()

        ]


    # ==========================================
    # CHECK
    # ==========================================

    def check(self, query, faq_id):

        if not self.loaded:

            return {

                "score":0,

                "positive_hits":[],

                "negative_hits":[]

            }


        query = text_processor.normalize(
            query
        )


        positive_hits = []

        negative_hits = []


        for rule in self.rules:


            if rule["faq_id"] != faq_id:

                continue


            for signal in rule["positive"]:

                if signal in query:

                    positive_hits.append(
                        signal
                    )


            for signal in rule["negative"]:

                if signal in query:

                    negative_hits.append(
                        signal
                    )


        score = 0


        # positive reward

        score += len(
            positive_hits
        ) * 0.15


        # negative penalty

        score -= len(
            negative_hits
        ) * 0.20



        return {

            "score":
                score,

            "positive_hits":
                positive_hits,

            "negative_hits":
                negative_hits

        }



    # ==========================================
    # STATISTICS
    # ==========================================

    def total(self):

        return len(
            self.rules
        )


boundary_service = BoundaryService()