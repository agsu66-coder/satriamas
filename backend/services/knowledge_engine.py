
import time

from models.search_result import SearchResult
from models.knowledge_item import KnowledgeItem
from services.keyword_service import keyword_service
from services.boundary_service import boundary_service

from services.knowledge_service import (
    knowledge_service
)

from services.semantic_service import semantic_service

from services.text_processor import (
    text_processor
)

from constants import (
    MIN_KEYWORD_SCORE,
    SEMANTIC_THRESHOLD
)

class KnowledgeEngine:

    # ==========================================
    # INIT
    # ==========================================

    def __init__(self):

        self.loaded = False

    # ==========================================
    # LOAD
    # ==========================================

    def load(self):
        """
        Memuat seluruh knowledge
        beserta semantic embedding.
        """

        knowledge_service.load()

        semantic_service.load()

        keyword_service.load()

        boundary_service.load()

        self.loaded = True

        return True

    # ==========================================
    # RELOAD
    # ==========================================

    def reload(self):
        """
        Reload workbook kemudian
        rebuild semantic embedding.
        """

        knowledge_service.reload()

        semantic_service.reload()

        self.loaded = True

        return True

    # ==========================================
    # READY
    # ==========================================

    def ready(self):

        return self.loaded

    # ==========================================
    # TOTAL
    # ==========================================

    def total(self):

        return knowledge_service.total()

    # ==========================================
    # STATISTICS
    # ==========================================

    def statistics(self):

        return {

            "knowledge":
                knowledge_service.statistics(),

            "semantic":
                semantic_service.statistics(),

            "keyword":
                keyword_service.loaded,

            "boundary":
                boundary_service.total()

        }

    # ==========================================
    # BUILD RESULT
    # ==========================================

    def _build_result(
        self,
        *,
        found=False,
        method="",
        score=0.0,
        matched_text="",
        row=None,
        message="",
        processing_time=0.0
    ):
        """
        Factory SearchResult.
        Seluruh hasil pencarian HARUS
        melalui method ini.
        """

        result = SearchResult()

        result.found = found
        result.method = method
        result.score = score
        result.matched_text = matched_text
        result.processing_time = processing_time
        result.message = message

        if row is not None:

            result.knowledge = (
                KnowledgeItem.from_dict(row)
            )

        else:

            result.knowledge = None

        return result
    # ==================================================
    # ITER ACTIVE RECORDS
    # ==================================================

    def _iter_active_records(self):
        """
        Iterator seluruh FAQ aktif.
        """

        for row in knowledge_service.get_records():

            status = str(
                row.get("Status", "")
            ).strip().upper()

            if status == "AKTIF":

                yield row

    # ==================================================
    # TOKENIZE
    # ==================================================

    def _tokenize(self, text):
        """
        Normalisasi kemudian
        memecah kalimat menjadi token.
        """

        text = text_processor.normalize(text)

        return [

            token

            for token in text.split()

            if token

        ]

    # ==================================================
    # EXACT MATCH
    # ==================================================

    def _exact_match(self, query):
        """
        Prioritas pertama.

        Mencari kecocokan persis pada:
        - Keyword
        - Variasi_*
        """

        query = text_processor.normalize(query)

        for row in self._iter_active_records():

            # ----------------------------------
            # Keyword
            # ----------------------------------

            keyword_text = str(
                row.get("Keyword", "")
            ).strip()

            if keyword_text:

                for keyword in keyword_text.split(";"):

                    keyword = text_processor.normalize(
                        keyword.strip()
                    )

                    if keyword == query:

                        return self._build_result(

                            found=True,

                            method="exact",

                            score=1.0,

                            matched_text=keyword,

                            row=row,

                            message="Exact keyword match"

                        )

            # ----------------------------------
            # Variasi
            # ----------------------------------

            for column, value in row.items():

                if not column.startswith("Variasi_"):

                    continue

                value = text_processor.normalize(
                    str(value)
                )

                if value == query:

                    return self._build_result(

                        found=True,

                        method="exact",

                        score=1.0,

                        matched_text=value,

                        row=row,

                        message=f"Exact {column}"

                    )

        return None
    # ==================================================
    # KEYWORD MATCH
    # ==================================================

    def _keyword_match(self, query):
        """
        Pencarian berdasarkan keyword dan variasi.

        Skor:
            +3  phrase match
            +1  token unik

        Seluruh Keyword dan Variasi dianggap
        sebagai phrase pencarian.
        """

        query = text_processor.normalize(query)

        query_tokens = set(
            self._tokenize(query)
        )

        best_row = None
        best_score = 0
        best_phrase = ""

        for row in self._iter_active_records():

            score = 0
            matched_phrase = ""

            matched_tokens = set()

            # ----------------------------------
            # Bangun seluruh phrase
            # ----------------------------------

            phrases = []

            keyword_text = str(
                row.get("Keyword", "")
            ).strip()

            if keyword_text:

                phrases.extend(

                    [
                        item.strip()

                        for item in keyword_text.split(";")

                        if item.strip()
                    ]

                )

            for column, value in row.items():

                if column.startswith("Variasi_"):

                    value = str(value).strip()

                    if value:

                        phrases.append(value)

            # ----------------------------------
            # Hitung skor
            # ----------------------------------

            for phrase in phrases:

                phrase = text_processor.normalize(
                    phrase
                )

                if not phrase:
                    continue

                # ==============================
                # Phrase Match
                # ==============================

                if phrase in query:

                    score += 3

                    if not matched_phrase:

                        matched_phrase = phrase

                # ==============================
                # Token Match
                # ==============================

                phrase_tokens = self._tokenize(
                    phrase
                )

                for token in phrase_tokens:

                    if (
                        token in query_tokens
                        and token not in matched_tokens
                    ):

                        score += 1

                        matched_tokens.add(token)

            # ----------------------------------
            # Simpan skor terbaik
            # ----------------------------------

            if score > best_score:

                best_score = score
                best_row = row
                best_phrase = matched_phrase

        # ----------------------------------
        # Tidak ditemukan
        # ----------------------------------

        if best_row is None:

            return None

        if best_score < 1:

            return None

        return self._build_result(

            found=True,

            method="keyword",

            score=float(best_score),

            matched_text=best_phrase,

            row=best_row,

            message=f"Keyword score = {best_score}"

        )
    # ==================================================
    # SEMANTIC MATCH
    # ==================================================

    def _semantic_match(self, query):
        """
        Tahap terakhir pencarian.

        Menggunakan SentenceTransformer apabila
        Exact Match dan Keyword Match tidak
        menemukan hasil.
        """

        result = semantic_service.search(query)

        if result is None:

            return None

        if result["score"] < SEMANTIC_THRESHOLD:

            return None

        return self._build_result(

            found=True,

            method="semantic",

            score=result["score"],

            matched_text="semantic",

            row=result["row"],

            message="Semantic Search"

        )

    # ==================================================
    # SEARCH
    # ==================================================

    def search(self, query):

        """
        Pipeline pencarian utama.

        Priority:

        1. Exact Match
        2. Keyword Match
        3. Semantic Match
        """

        start = time.perf_counter()

        # ----------------------------------
        # Exact
        # ----------------------------------

        result = self._exact_match(query)

        if result:

            result.processing_time = (
                time.perf_counter() - start
            )

            return result

        # ----------------------------------
        # Keyword
        # ----------------------------------

        result = self._keyword_match(query)

        if result:

            if result.score >= MIN_KEYWORD_SCORE:

                result.processing_time = (
                    time.perf_counter() - start
                )    

                return result

        # ----------------------------------
        # Semantic
        # ----------------------------------

        result = self._semantic_match(query)

        if result:
           
            result.processing_time = (
                time.perf_counter() - start
            )
            return result
          

        # ----------------------------------
        # Not Found
        # ----------------------------------

        return self._build_result(

            found=False,

            method="",

            score=0.0,

            message="Knowledge tidak ditemukan.",

            processing_time=(
                time.perf_counter() - start
            )

        )
# ==================================================
# SINGLETON
# ==================================================

knowledge_engine = KnowledgeEngine()