from sentence_transformers import util
from services.knowledge_service import knowledge_service


class KnowledgeConflictAnalyzer:


    def __init__(self):

        self.conflicts = []


    # ======================================
    # ANALYZE
    # ======================================

    def analyze(
        self,
        embeddings,
        threshold=0.70
    ):

        self.conflicts.clear()


        data = (
            knowledge_service
            .get_training_data()
        )


        total = len(data)


        for i in range(total):

            for j in range(i+1,total):


                score = float(
                    util.cos_sim(
                        embeddings[i],
                        embeddings[j]
                    )
                )


                if score >= threshold:


                    self.conflicts.append({

                        "faq_1":
                            data[i]["key"],

                        "faq_2":
                            data[j]["key"],

                        "category_1":
                            data[i]["category"],

                        "category_2":
                            data[j]["category"],

                        "score":
                            round(score,4)

                    })


        return self.conflicts



    # ======================================
    # RESULT
    # ======================================

    def get_result(self):

        return self.conflicts



knowledge_conflict = KnowledgeConflictAnalyzer()