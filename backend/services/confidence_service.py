class ConfidenceService:


    def __init__(self):

        # batas confidence
        self.high_threshold = 0.70
        self.medium_threshold = 0.40



    def evaluate(self, result):


        if result is None:

            return {

                "level": "LOW",
                "score": 0

            }



        score = result.get(
            "final_score",
            0
        )



        if score >= self.high_threshold:

            level = "HIGH"


        elif score >= self.medium_threshold:

            level = "MEDIUM"


        else:

            level = "LOW"



        return {

            "level": level,
            "score": score

        }



confidence_service = ConfidenceService()