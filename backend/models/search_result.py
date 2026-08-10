"""
TERATAI AI

Model : SearchResult
Version : 1.0.0

Representasi hasil pencarian Knowledge Engine.
"""

from dataclasses import dataclass, field
from typing import Optional
from models.knowledge_item import KnowledgeItem


@dataclass
class SearchResult:

    VERSION = "1.0.0"

    # ======================================
    # Status Hasil
    # ======================================

    found: bool = False

    method: str = ""

    score: float = 0.0

    # ======================================
    # Data yang ditemukan
    # ======================================

    knowledge: Optional[KnowledgeItem] = None

    matched_text: str = ""

    # ======================================
    # Statistik
    # ======================================

    processing_time: float = 0.0

    # ======================================
    # Informasi Tambahan
    # ======================================

    message: str = ""

    # ======================================

    @property
    def answer(self):

        if self.knowledge is None:
            return ""

        return self.knowledge.answer

    # ======================================

    @property
    def knowledge_id(self):

        if self.knowledge is None:
            return ""

        return self.knowledge.id

    # ======================================

    @property
    def category(self):

        if self.knowledge is None:
            return ""

        return self.knowledge.category

    # ======================================

    def to_dict(self):

        return {

            "found": self.found,

            "method": self.method,

            "score": round(self.score, 4),

            "knowledge_id": self.knowledge_id,

            "category": self.category,

            "matched_text": self.matched_text,

            "processing_time": round(
                self.processing_time,
                3
            ),

            "message": self.message,

            "answer": self.answer

        }

    # ======================================

    def __bool__(self):

        return self.found

    # ======================================

    def __str__(self):

        if not self.found:

            return "[NOT FOUND]"

        return (
            f"[{self.method}] "
            f"{self.knowledge_id} "
            f"({self.score:.3f})"
        )