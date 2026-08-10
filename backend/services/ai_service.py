"""
==================================================
TERATAI AI

AI Service
Version : 1.0.0
Status  : STABLE

Layer percakapan TERATAI AI.

Arsitektur

User
 │
 ▼
AIService
 │
 ├── Greeting
 ├── Thanks
 ├── Goodbye
 ├── Help
 └── ConversationService

Knowledge search tetap dilakukan oleh
ConversationService dan KnowledgeEngine.

==================================================
"""

from models.ai_response import AIResponse
from services.conversation_service import conversation_service


class AIService:

    def __init__(self):

        # ----------------------------------
        # Greeting
        # ----------------------------------

        self._greetings = {

            "halo",
            "hai",
            "hi",
            "hello",

            "selamat pagi",
            "selamat siang",
            "selamat sore",
            "selamat malam",

            "assalamualaikum",
            "assalamu'alaikum",
            "assalamu alaikum"

        }

        # ----------------------------------
        # Thanks
        # ----------------------------------

        self._thanks = {

            "terima kasih",
            "makasih",
            "thanks",
            "thank you",
            "thx"

        }

        # ----------------------------------
        # Goodbye
        # ----------------------------------

        self._goodbye = {

            "bye",
            "dadah",
            "selamat tinggal",
            "sampai jumpa",
            "see you"

        }

        # ----------------------------------
        # Help
        # ----------------------------------

        self._helps = {

            "help",
            "bantuan",
            "tolong",
            "menu",
            "bisa apa",
            "apa yang bisa kamu lakukan"

        }

    # ==================================================
    # NORMALIZE
    # ==================================================

    def _normalize(self, text):

        if text is None:

            return ""

        return str(text).strip().lower()

    # ==================================================
    # TEMPLATE RESPONSE
    # ==================================================

    def _template(
        self,
        text,
        category
    ):

        return AIResponse(

            success=True,

            text=text,

            category=category,

            method="template",

            confidence=1.0

        )

    # ==================================================
    # GREETING
    # ==================================================

    def _is_greeting(self, text):

        return text in self._greetings

    # ==================================================
    # THANKS
    # ==================================================

    def _is_thanks(self, text):

        return text in self._thanks

    # ==================================================
    # GOODBYE
    # ==================================================

    def _is_goodbye(self, text):

        return text in self._goodbye

    # ==================================================
    # HELP
    # ==================================================

    def _is_help(self, text):

        return text in self._helps

    # ==================================================
    # REPLY
    # ==================================================

    def reply(self, message):

        text = self._normalize(message)

        # ----------------------------------
        # Empty
        # ----------------------------------

        if not text:

            return self._template(

                "Silakan tuliskan pertanyaan yang ingin Anda ajukan.",

                "Empty"

            )

        # ----------------------------------
        # Greeting
        # ----------------------------------

        if self._is_greeting(text):

            return self._template(

                (
                    "Halo, selamat datang di TERATAI AI.\n\n"
                    "Saya siap membantu menjawab pertanyaan "
                    "seputar pelayanan Kecamatan."
                ),

                "Greeting"

            )

        # ----------------------------------
        # Thanks
        # ----------------------------------

        if self._is_thanks(text):

            return self._template(

                "Sama-sama. Senang dapat membantu Anda.",

                "Thanks"

            )

        # ----------------------------------
        # Goodbye
        # ----------------------------------

        if self._is_goodbye(text):

            return self._template(

                (
                    "Terima kasih telah menggunakan "
                    "TERATAI AI.\n"
                    "Sampai jumpa kembali."
                ),

                "Goodbye"

            )

        # ----------------------------------
        # Help
        # ----------------------------------

        if self._is_help(text):

            return self._template(

                (
                    "Saya dapat membantu menjawab pertanyaan "
                    "mengenai pelayanan Kecamatan.\n\n"

                    "Contoh:\n"

                    "• Cara membuat KTP\n"
                    "• Mengurus Kartu Keluarga\n"
                    "• Persyaratan surat\n"
                    "• Pelayanan Kecamatan\n"
                    "• Pengaduan pelayanan"
                ),

                "Help"

            )

        # ----------------------------------
        # Knowledge Engine
        # ----------------------------------

        return conversation_service.reply(message)


# ==================================================
# Singleton
# ==================================================

ai_service = AIService()