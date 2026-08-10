from services.semantic_service import semantic_service
from services.boundary_service import boundary_service
from services.keyword_service import keyword_service
from services.confidence_service import confidence_service
from services.knowledge_service import knowledge_service


class ReasoningService:

    def __init__(self):

        self.semantic_weight = 0.45
        self.keyword_weight = 0.35
        self.boundary_weight = 0.2

        self.loaded = False

    # ==========================================
    # LOAD
    # ==========================================

    def load(self):

        knowledge_service.load()

        semantic_service.load()

        keyword_service.load()

        boundary_service.load()

        self.loaded = True

        return True

    # ==========================================
    # MERGE CANDIDATE
    # ==========================================

    def merge_candidates(
        self,
        semantic_candidates,
        keyword_candidates
    ):

        merged = {}

        # --------------------------
        # SEMANTIC
        # --------------------------

        for item in semantic_candidates:

            faq_id = item["row"].get(
                "ID",
                ""
            )

            merged[faq_id] = {

                "row":
                    item["row"],

                "semantic_score":
                    item.get(
                        "score",
                        0
                    ),

                "keyword_score":
                    0

            }

        # --------------------------
        # KEYWORD
        # --------------------------

        for item in keyword_candidates:

            faq_id = item["row"].get(
                "ID",
                ""
            )

            if faq_id in merged:

                merged[faq_id]["keyword_score"] = (

                    item.get(
                        "keyword_score",
                        0
                    )

                )

            else:

                merged[faq_id] = {

                    "row":
                        item["row"],

                    "semantic_score":
                        0,

                    "keyword_score":
                        item.get(
                            "keyword_score",
                            0
                        )

                }

        return list(
            merged.values()
        )

    # ==========================================
    # SEARCH
    # ==========================================

    def search(
        self,
        query
    ):

        if not self.loaded:

            self.load()

        semantic_candidates = semantic_service.search_candidates(

            query,

            limit=10

        )

        keyword_candidates = keyword_service.search_candidates(

            query,

            limit=10

        )

        candidates = self.merge_candidates(

            semantic_candidates,

            keyword_candidates

        )

        if not candidates:

            return None

        results = []

        for item in candidates:

            faq = item["row"]

            faq_id = faq.get(
                "ID",
                ""
            )

            semantic_score = item.get(
                "semantic_score",
                0
            )

            keyword_score = item.get(
                "keyword_score",
                0
            )

            if keyword_score > 0:

                keyword_score = keyword_score * 2

            boundary = boundary_service.check(

                query,

                faq_id

            )

            boundary_score = boundary.get(

                "score",

                0

            )

            final_score = (

                semantic_score *
                self.semantic_weight

            ) + (

                keyword_score *
                self.keyword_weight

            ) + (

                boundary_score *
                self.boundary_weight

            )

            # --------------------------
            # NEGATIVE BOUNDARY
            # --------------------------

            if len(boundary["negative_hits"]) > 0:

                final_score -= 0.3

            # --------------------------
            # POSITIVE BOUNDARY
            # --------------------------

            if len(boundary["positive_hits"]) > 0:

                final_score += 0.25

            print(
                faq_id,
                "SEM:",
                semantic_score,
                "KEY:",
                keyword_score,
                "BOUND:",
                boundary_score,
                "FINAL:",
                final_score
            )

            results.append({

                "faq_id":
                    faq_id,

                "semantic_score":
                    semantic_score,

                "keyword_score":
                    keyword_score,

                "boundary_score":
                    boundary_score,

                "final_score":
                    final_score,

                "boundary":
                    boundary,

                "row":
                    faq

            })

        results.sort(

            key=lambda x: x["final_score"],

            reverse=True

        )

        best_result = results[0]

        confidence = confidence_service.evaluate(
            best_result
        )

        best_result["confidence"] = confidence

        # ==========================================
        # MEDIUM CANDIDATES
        # ==========================================

        if confidence["level"] == "MEDIUM":

            best_result["candidates"] = results[:2]

        else:

            best_result["candidates"] = []

        return best_result


reasoning_service = ReasoningService()