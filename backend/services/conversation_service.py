from models.ai_response import AIResponse

from services.reasoning_service import (
    reasoning_service
)

from services.confidence_service import (
    confidence_service
)


class ConversationService:

    def __init__(self):

        pass

    # ======================================
    # REPLY
    # ======================================

    def reply(
        self,
        message: str
    ) -> AIResponse:

        result = reasoning_service.search(
            message
        )

        print("=" * 60)
        print("REASONING RESULT")
        print(result)
        print("=" * 60)

        # ----------------------------------
        # Tidak ada kandidat
        # ----------------------------------

        if result is None:

            return AIResponse(

                success=False,

                text=(
                    "Maaf, saya belum menemukan "
                    "jawaban atas pertanyaan tersebut."
                ),

                method="not_found",

                confidence=0.0

            )

        # ----------------------------------
        # Confidence Evaluation
        # ----------------------------------

        confidence = (
            result.get(
                "confidence",
                {}
            )
        )

        level = confidence.get(
            "level",
            "LOW"
        )

        score = confidence.get(
            "score",
            0
        )

        # ----------------------------------
        # LOW
        # ----------------------------------

        if level == "LOW":

            return AIResponse(

                success=False,

                text=(
                    "Maaf, saya belum cukup yakin "
                    "dengan informasi yang sesuai "
                    "dengan pertanyaan Anda.\n\n"

                    "Untuk mendapatkan informasi yang "
                    "tepat, Anda dapat menghubungi "
                    "petugas melalui layanan Pengaduan.\n\n"

                    "Silakan pilih menu Pengaduan "
                    "untuk melanjutkan."
                ),

                method="confidence_low",

                confidence=score

            )

        # ----------------------------------
        # MEDIUM
        # ----------------------------------

        if level == "MEDIUM":

            candidates = result.get(
                "candidates",
                []
            )

            if len(candidates) >= 2:

                candidate_1 = candidates[0]["row"]

                candidate_2 = candidates[1]["row"]

                # ==================================
                # AMBIL KEYWORD UTAMA
                # ==================================

                keyword_1 = str(
                    candidate_1.get(
                        "Keyword",
                        ""
                    )
                ).strip()

                keyword_2 = str(
                    candidate_2.get(
                        "Keyword",
                        ""
                    )
                ).strip()

                # ----------------------------------
                # Jika terdapat beberapa keyword
                # yang dipisahkan tanda ;
                # gunakan keyword pertama.
                # ----------------------------------

                if ";" in keyword_1:

                    keyword_1 = (
                        keyword_1
                        .split(";")[0]
                        .strip()
                    )

                if ";" in keyword_2:

                    keyword_2 = (
                        keyword_2
                        .split(";")[0]
                        .strip()
                    )

                # ==================================
                # KATEGORI
                # ==================================

                category_1 = str(
                    candidate_1.get(
                        "Kategori",
                        ""
                    )
                ).strip()

                category_2 = str(
                    candidate_2.get(
                        "Kategori",
                        ""
                    )
                ).strip()

                # ==================================
                # BENTUK INFORMASI
                # ==================================

                if (

                    category_1 and

                    category_2 and

                    category_1.lower()
                    == category_2.lower()

                ):

                    option_1 = (
                        f"{category_1} "
                        f"karena {keyword_1}"
                    )

                    option_2 = (
                        f"{category_2} "
                        f"karena {keyword_2}"
                    )

                else:

                    option_1 = (

                        keyword_1
                        if keyword_1

                        else category_1

                    )

                    option_2 = (

                        keyword_2
                        if keyword_2

                        else category_2

                    )

                # ==================================
                # PESAN KLARIFIKASI
                # ==================================

                text = (

                    "Saya menemukan dua informasi "
                    "yang kemungkinan sesuai dengan "
                    "pertanyaan Anda, apakah Anda "
                    "sedang membutuhkan informasi tentang:\n\n"

                    f"1. {option_1}?\n"
                    f"2. {option_2}?\n\n"

                    "Silakan pilih nomor sesuai pilihan Anda.\n"

                    "Silakan ketik 0 untuk menjelaskan "
                    "kembali kebutuhan Anda. Terima Kasih."
                )

                return AIResponse(

                    success=True,

                    text=text,

                    category="",

                    method="confidence_medium",

                    confidence=score,

                    candidates=[

                        candidate_1,

                        candidate_2

                    ]

                )

            # ----------------------------------
            # MEDIUM TANPA 2 KANDIDAT
            # ----------------------------------

            return AIResponse(

                success=False,

                text=(
                    "Maaf, saya belum cukup yakin "
                    "dengan informasi yang sesuai "
                    "dengan pertanyaan Anda.\n\n"

                    "Silakan jelaskan kembali "
                    "kebutuhan Anda."
                ),

                method="confidence_medium",

                confidence=score

            )

        # ----------------------------------
        # HIGH
        # ----------------------------------

        row = result["row"]

        return AIResponse(

            success=True,

            text=row.get(
                "Jawaban",
                ""
            ),

            category=row.get(
                "Kategori",
                ""
            ),

            method="reasoning",

            confidence=score

        )


conversation_service = ConversationService()
