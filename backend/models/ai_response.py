"""
==================================================
TERATAI AI

AI Response Model
Version : 1.1.0

Model hasil balasan AI kepada user.

Digunakan oleh ConversationService,
AIService, Flask API, dan WhatsApp Bot.

==================================================
"""

from dataclasses import dataclass, field


@dataclass
class AIResponse:

    VERSION = "1.1.0"

    # ======================================
    # Status
    # ======================================

    success: bool = False

    # ======================================
    # Isi balasan
    # ======================================

    text: str = ""

    # ======================================
    # Metadata
    # ======================================

    category: str = ""

    method: str = ""

    confidence: float = 0.0

    # ======================================
    # Kandidat Klarifikasi
    # ======================================

    candidates: list = field(
        default_factory=list
    )

    # ======================================

    def to_dict(self):

        return {

            "success": self.success,

            "text": self.text,

            "category": self.category,

            "method": self.method,

            "confidence": round(
                self.confidence,
                4
            ),

            "candidates": self.candidates

        }

    # ======================================

    def __bool__(self):

        return self.success

    # ======================================

    def __str__(self):

        return self.text