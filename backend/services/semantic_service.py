from sentence_transformers import SentenceTransformer
from sentence_transformers import (
    SentenceTransformer,
    util
)
from constants import MODEL_NAME
from constants import (
    MODEL_NAME,
    SEMANTIC_THRESHOLD
)
from services.knowledge_service import knowledge_service

class SemanticService:

    def __init__(self):

        self.model = None

        self.training_data = []

        self.embeddings = None

        self.loaded = False

        self.statistics_data = {}

    # ==================================================
    # LOAD MODEL
    # ==================================================

    def _load_model(self):

        if self.model is None:

            self.model = SentenceTransformer(
                MODEL_NAME
            )

    # ==================================================
    # BUILD EMBEDDINGS
    # ==================================================

    def _build_embeddings(self):

        self.training_data = (
            knowledge_service.get_training_data()
        )

        if not self.training_data:

            self.embeddings = None

            self.statistics_data = {

                "training": 0,
                "embedding": 0

            }

            return

        texts = [

            item["text"]

            for item in self.training_data

        ]

        self.embeddings = self.model.encode(

            texts,

            convert_to_tensor=True

        )

        self.statistics_data = {

            "training":
                len(self.training_data),

            "embedding":
                len(texts)

        }

    # ==================================================
    # LOAD
    # ==================================================

    def load(self):

        self._load_model()

        self._build_embeddings()

        self.loaded = (

            self.embeddings is not None

        )

        return self.loaded

    # ==================================================
    # RELOAD
    # ==================================================

    def reload(self):

        self._build_embeddings()

        self.loaded = (

            self.embeddings is not None

        )

        return self.loaded
    # ==================================================
    # READY
    # ==================================================

    def ready(self):

        return self.loaded

    # ==================================================
    # TOTAL
    # ==================================================

    def total(self):

        return len(
            self.training_data
        )

    # ==================================================
    # STATISTICS
    # ==================================================

    def statistics(self):

        return self.statistics_data

    # ==================================================
    # SEARCH
    # ==================================================

    def search(self, query):
        """
        Semantic search.
        Mengembalikan dictionary jika ditemukan.
        """

        if not self.loaded:
            return None

        embedding = self._encode_query(query)

        index, score = self._best_match(
            embedding
        )

        if index is None:
            return None

        if score < SEMANTIC_THRESHOLD:
            return None

        training = self.training_data[index]

        row = knowledge_service.find_by_key(
            training["key"]
        )

        return {

            "found": True,

            "index": index,

            "score": score,

            "row": row

        }
    # ==================================================
    # ENCODE QUERY
    # ==================================================

    def _encode_query(self, query):
        """
        Mengubah query menjadi embedding.
        """

        if not self.loaded:
            return None

        query = query.strip()

        if not query:
            return None

        return self.model.encode(
            query,
            convert_to_tensor=True
        )
    # ==================================================
    # BEST MATCH
    # ==================================================

    def _best_match(self, query_embedding):
        """
        Mengembalikan index FAQ dan skor similarity tertinggi.
        """

        if query_embedding is None:
            return None, 0.0

        if self.embeddings is None:
            return None, 0.0

        scores = util.cos_sim(
            query_embedding,
            self.embeddings
        )[0]

        best_index = scores.argmax().item()

        best_score = float(
            scores[best_index]
        )

        return best_index, best_score

    # ==================================================
    # SEARCH CANDIDATES
    # ==================================================

    def search_candidates(
            self,
            query,
            limit=20
    ):
        """
        Mengembalikan beberapa kandidat FAQ
        berdasarkan semantic similarity.
        Digunakan oleh Reasoning Engine.
        """

        if not self.loaded:

            return []


        embedding = self._encode_query(
            query
        )


        if embedding is None:

            return []


        scores = util.cos_sim(
            embedding,
            self.embeddings
        )[0]


        ranked = sorted(

            enumerate(
                scores.tolist()
            ),

            key=lambda x:x[1],

            reverse=True

        )


        results = []


        for index, score in ranked[:limit]:


            score = float(score)


            if score < 0.2:

                continue


            training = self.training_data[index]


            row = knowledge_service.find_by_key(

                training["key"]

            )


            results.append({

                "index":
                    index,

                "score":
                    score,

                "row":
                    row

            })


        return results

semantic_service = SemanticService()