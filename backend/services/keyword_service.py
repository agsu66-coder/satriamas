from services.knowledge_service import knowledge_service
from services.text_processor import text_processor


class KeywordService:


    def __init__(self):

        self.training_data = []

        self.loaded = False



    # ==========================================
    # LOAD
    # ==========================================

    def load(self):

        self.training_data = (
            knowledge_service.get_training_data()
        )

        self.loaded = True

        return True



    # ==========================================
    # SEARCH KEYWORD
    # ==========================================

    def search_candidates(
            self,
            query,
            limit=10
    ):

        if not self.loaded:

            return []


        query = text_processor.normalize(
            query
        )


        query_words = set(
            query.split()
        )


        results = []


        for item in self.training_data:


            text = text_processor.normalize(
                item["text"]
            )


            training_words = set(
                text.split()
            )


            matched = []


            for word in query_words:

                if word in training_words:

                    matched.append(
                        word
                    )


            if not matched:

                continue



            # =================================
            # SCORE
            # =================================

            score = (

                len(matched)
                /
                len(query_words)

            )



            row = knowledge_service.find_by_key(

                item["key"]

            )


            results.append({

                "index":
                    item["key"],


                "keyword_score":
                    score,


                "matched_keywords":
                    matched,


                "row":
                    row

            })



        results.sort(

            key=lambda x:
                x["keyword_score"],

            reverse=True

        )


        return results[:limit]


keyword_service = KeywordService()