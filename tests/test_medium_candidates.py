"""
==================================================
TERATAI AI

Offline Medium Candidate Test
Version : 1.0.2

Tujuan:
Menguji alur CONFIDENCE MEDIUM pada
ConversationService.

Test memastikan:

1. Response berhasil.
2. Method = confidence_medium.
3. Terdapat 2 kandidat.
4. Kandidat pertama berbeda dengan kandidat kedua.
5. Keyword kandidat pertama muncul.
6. Keyword kandidat kedua muncul.
7. Pilihan nomor 1 dan 2 muncul.
8. Opsi 0 muncul.

Test ini tidak menggunakan:

- WhatsApp
- Flask
- Excel
- Knowledge Engine asli

ReasoningService digantikan sementara
dengan MockReasoningService.

==================================================
"""


# ==================================================
# IMPORT SYSTEM
# ==================================================

import os
import sys


# ==================================================
# PATH PROJECT
# ==================================================

# Lokasi:
#
# E:\Teratai Proyek\v0.2\tests
#
# Project root:
#
# E:\Teratai Proyek\v0.2
#
# Backend:
#
# E:\Teratai Proyek\v0.2\backend
#

PROJECT_ROOT = os.path.abspath(

    os.path.join(

        os.path.dirname(__file__),

        ".."

    )

)


BACKEND_ROOT = os.path.join(

    PROJECT_ROOT,

    "backend"

)


# ==================================================
# MASUKKAN BACKEND KE PYTHON PATH
# ==================================================

if BACKEND_ROOT not in sys.path:

    sys.path.insert(

        0,

        BACKEND_ROOT

    )


# ==================================================
# IMPORT CONVERSATION SERVICE
# ==================================================

from services.conversation_service import (
    ConversationService
)


# ==================================================
# MOCK REASONING SERVICE
# ==================================================

class MockReasoningService:


    def search(
        self,
        message
    ):

        # ------------------------------------------
        # Kandidat pertama
        # ------------------------------------------

        candidate_1 = {

            "row": {

                "ID":
                    "FAQ-004",

                "Kategori":
                    "KTP-el",

                "Keyword":
                    "ktp rusak",

                "Variasi_1":
                    "e ktp rusak",

                "Variasi_2":
                    "ganti ktp rusak",

                "Jawaban":
                    (
                        "Untuk penerbitan KTP-el "
                        "karena rusak, siapkan dokumen."
                    )

            },

            "final_score":
                0.55

        }


        # ------------------------------------------
        # Kandidat kedua
        # ------------------------------------------

        candidate_2 = {

            "row": {

                "ID":
                    "FAQ-005",

                "Kategori":
                    "KTP-el",

                "Keyword":
                    "ktp hilang",

                "Variasi_1":
                    "e ktp hilang",

                "Variasi_2":
                    "ganti ktp hilang",

                "Jawaban":
                    (
                        "Untuk penerbitan KTP-el "
                        "karena hilang, siapkan dokumen."
                    )

            },

            "final_score":
                0.52

        }


        # ------------------------------------------
        # Hasil reasoning
        # ------------------------------------------

        return {

            "row":
                candidate_1["row"],

            "confidence": {

                "level":
                    "MEDIUM",

                "score":
                    0.55

            },

            "candidates": [

                candidate_1,

                candidate_2

            ]

        }


# ==================================================
# TEST MEDIUM CANDIDATES
# ==================================================

def test_medium_candidates():


    print()

    print(
        "=" * 60
    )

    print(
        "TERATAI AI"
    )

    print(
        "OFFLINE MEDIUM CANDIDATE TEST"
    )

    print(
        "=" * 60
    )


    # ==================================================
    # IMPORT MODULE CONVERSATION SERVICE
    # ==================================================

    from services import conversation_service as module


    # ==================================================
    # SIMPAN REASONING SERVICE ASLI
    # ==================================================

    original_reasoning_service = (

        module.reasoning_service

    )


    # ==================================================
    # GANTI DENGAN MOCK
    # ==================================================

    module.reasoning_service = (

        MockReasoningService()

    )


    try:


        # ==========================================
        # BUAT SERVICE
        # ==========================================

        service = ConversationService()


        # ==========================================
        # SIMULASI PERTANYAAN WARGA
        # ==========================================

        response = service.reply(

            "Cara cetak KTP"

        )


        # ==========================================
        # TAMPILKAN RESPONSE
        # ==========================================

        print()

        print(
            "=" * 60
        )

        print(
            "HASIL RESPONSE"
        )

        print(
            "=" * 60
        )

        print()

        print(
            response.text
        )

        print()


        # ==================================================
        # TEST 1
        # ==================================================

        if response.success:

            print(
                "[PASS] success = True"
            )

        else:

            print(
                "[FAIL] success seharusnya True"
            )


        # ==================================================
        # TEST 2
        # ==================================================

        if (

            response.method
            ==
            "confidence_medium"

        ):

            print(
                "[PASS] method = confidence_medium"
            )

        else:

            print(
                "[FAIL] method bukan confidence_medium"
            )


        # ==================================================
        # TEST 3
        # ==================================================

        if (

            len(
                response.candidates
            )
            ==
            2

        ):

            print(
                "[PASS] jumlah kandidat = 2"
            )

        else:

            print(
                "[FAIL] jumlah kandidat bukan 2"
            )


        # ==================================================
        # AMBIL KANDIDAT
        # ==================================================

        candidate_1 = (

            response.candidates[0]

            if len(
                response.candidates
            ) >= 1

            else {}

        )


        candidate_2 = (

            response.candidates[1]

            if len(
                response.candidates
            ) >= 2

            else {}

        )


        # ==================================================
        # TEST 4
        # ==================================================

        id_1 = str(

            candidate_1.get(
                "ID",
                ""
            )

        ).strip()


        id_2 = str(

            candidate_2.get(
                "ID",
                ""
            )

        ).strip()


        if (

            id_1
            and
            id_2
            and
            id_1 != id_2

        ):

            print(
                "[PASS] kandidat pertama dan kedua berbeda"
            )

        else:

            print(
                "[FAIL] kandidat pertama dan kedua sama"
            )


        # ==================================================
        # TEST 5
        # ==================================================

        if (

            "ktp rusak"
            in
            response.text.lower()

        ):

            print(
                "[PASS] kandidat 'ktp rusak' muncul"
            )

        else:

            print(
                "[FAIL] kandidat 'ktp rusak' tidak muncul"
            )


        # ==================================================
        # TEST 6
        # ==================================================

        if (

            "ktp hilang"
            in
            response.text.lower()

        ):

            print(
                "[PASS] kandidat 'ktp hilang' muncul"
            )

        else:

            print(
                "[FAIL] kandidat 'ktp hilang' tidak muncul"
            )


        # ==================================================
        # TEST 7
        # ==================================================

        if (

            "1."
            in
            response.text

            and

            "2."
            in
            response.text

        ):

            print(
                "[PASS] pilihan nomor 1 dan 2 muncul"
            )

        else:

            print(
                "[FAIL] pilihan nomor 1 dan 2 tidak lengkap"
            )


        # ==================================================
        # TEST 8
        # ==================================================

        if (

            "ketik 0"
            in
            response.text.lower()

        ):

            print(
                "[PASS] opsi 0 muncul"
            )

        else:

            print(
                "[FAIL] opsi 0 tidak muncul"
            )


        # ==================================================
        # TEST 9
        # ==================================================

        if (

            id_1 == "FAQ-004"

        ):

            print(
                "[PASS] kandidat pertama = FAQ-004"
            )

        else:

            print(
                "[FAIL] kandidat pertama bukan FAQ-004"
            )


        # ==================================================
        # TEST 10
        # ==================================================

        if (

            id_2 == "FAQ-005"

        ):

            print(
                "[PASS] kandidat kedua = FAQ-005"
            )

        else:

            print(
                "[FAIL] kandidat kedua bukan FAQ-005"
            )


        # ==================================================
        # STATUS AKHIR
        # ==================================================

        print()

        print(
            "=" * 60
        )

        print(
            "HASIL AKHIR"
        )

        print(
            "=" * 60
        )


        all_pass = (

            response.success

            and

            response.method
            ==
            "confidence_medium"

            and

            len(
                response.candidates
            )
            ==
            2

            and

            id_1
            ==
            "FAQ-004"

            and

            id_2
            ==
            "FAQ-005"

            and

            id_1
            !=
            id_2

            and

            "ktp rusak"
            in
            response.text.lower()

            and

            "ktp hilang"
            in
            response.text.lower()

            and

            "1."
            in
            response.text

            and

            "2."
            in
            response.text

            and

            "ketik 0"
            in
            response.text.lower()

        )


        if all_pass:

            print(
                "STATUS : SEMUA TEST BERHASIL"
            )

        else:

            print(
                "STATUS : ADA TEST YANG GAGAL"
            )


        print(
            "=" * 60
        )


    finally:


        # ==================================================
        # KEMBALIKAN REASONING SERVICE ASLI
        # ==================================================

        module.reasoning_service = (

            original_reasoning_service

        )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    test_medium_candidates()