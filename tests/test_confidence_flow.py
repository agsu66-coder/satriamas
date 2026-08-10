"""
==================================================
TERATAI AI

Offline Confidence Flow Test
Version : 1.0.0

Pengujian alur:
    HIGH
    MEDIUM
    LOW

Test ini berdiri sendiri dan tidak membutuhkan
import dari project TERATAI.

==================================================
"""


# ==================================================
# SIMULASI CONVERSATION SERVICE
# ==================================================

def simulate_conversation(result):

    # ----------------------------------------------
    # Tidak ada hasil
    # ----------------------------------------------

    if result is None:

        return {

            "success": False,

            "text":
                "Maaf, saya belum menemukan "
                "jawaban atas pertanyaan tersebut.",

            "method":
                "not_found",

            "confidence":
                0.0,

            "candidates":
                []

        }


    # ----------------------------------------------
    # Confidence
    # ----------------------------------------------

    confidence = result.get(
        "confidence",
        {}
    )

    level = confidence.get(
        "level",
        "LOW"
    )

    score = confidence.get(
        "score",
        0
    )


    # ----------------------------------------------
    # LOW
    # ----------------------------------------------

    if level == "LOW":

        return {

            "success": False,

            "text": (
                "Maaf, saya belum cukup yakin "
                "dengan informasi yang sesuai "
                "dengan pertanyaan Anda.\n\n"

                "Untuk mendapatkan informasi yang "
                "tepat, Anda dapat menghubungi "
                "petugas melalui layanan Pengaduan.\n\n"

                "Silakan pilih menu Pengaduan "
                "untuk melanjutkan."
            ),

            "method":
                "confidence_low",

            "confidence":
                score,

            "candidates":
                []

        }


    # ----------------------------------------------
    # MEDIUM
    # ----------------------------------------------

    if level == "MEDIUM":

        candidates = result.get(
            "candidates",
            []
        )


        if len(candidates) >= 2:

            candidate_1 = candidates[0]["row"]

            candidate_2 = candidates[1]["row"]


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


            text = (

                "Saya menemukan dua informasi "
                "yang kemungkinan sesuai dengan "
                "pertanyaan Anda, apakah Anda "
                "sedang membutuhkan informasi tentang:\n\n"

                f"1. {category_1}?\n"
                f"2. {category_2}?\n\n"

                "Silakan pilih nomor sesuai pilihan Anda.\n"

                "Silakan ketik 0 untuk menjelaskan "
                "kembali kebutuhan Anda. Terima Kasih."
            )


            return {

                "success": True,

                "text":
                    text,

                "method":
                    "confidence_medium",

                "confidence":
                    score,

                "candidates":
                    [
                        candidate_1,
                        candidate_2
                    ]

            }


        return {

            "success": False,

            "text": (
                "Maaf, saya belum cukup yakin "
                "dengan informasi yang sesuai "
                "dengan pertanyaan Anda.\n\n"

                "Silakan jelaskan kembali "
                "kebutuhan Anda."
            ),

            "method":
                "confidence_medium",

            "confidence":
                score,

            "candidates":
                []

        }


    # ----------------------------------------------
    # HIGH
    # ----------------------------------------------

    row = result.get(
        "row",
        {}
    )


    return {

        "success": True,

        "text":
            row.get(
                "Jawaban",
                ""
            ),

        "category":
            row.get(
                "Kategori",
                ""
            ),

        "method":
            "reasoning",

        "confidence":
            score,

        "candidates":
            []

    }


# ==================================================
# TEST HELPER
# ==================================================

def check(
    name,
    condition
):

    if condition:

        print(
            f"[PASS] {name}"
        )

        return True

    print(
        f"[FAIL] {name}"
    )

    return False


# ==================================================
# TEST HIGH
# ==================================================

def test_high():

    print()
    print("=" * 60)
    print("TEST HIGH")
    print("=" * 60)


    result = {

        "confidence": {

            "level":
                "HIGH",

            "score":
                0.85

        },

        "row": {

            "ID":
                "FAQ001",

            "Kategori":
                "Kartu Keluarga",

            "Jawaban":
                "Persyaratan pembuatan Kartu Keluarga."

        }

    }


    response = simulate_conversation(
        result
    )


    passed = True


    passed &= check(
        "success = True",
        response["success"] is True
    )


    passed &= check(
        "method = reasoning",
        response["method"] == "reasoning"
    )


    passed &= check(
        "jawaban tersedia",
        response["text"] != ""
    )


    passed &= check(
        "tidak ada kandidat",
        len(response["candidates"]) == 0
    )


    return passed


# ==================================================
# TEST MEDIUM
# ==================================================

def test_medium():

    print()
    print("=" * 60)
    print("TEST MEDIUM")
    print("=" * 60)


    result = {

        "confidence": {

            "level":
                "MEDIUM",

            "score":
                0.55

        },

        "candidates": [

            {

                "row": {

                    "ID":
                        "FAQ001",

                    "Kategori":
                        "Persyaratan pembuatan Kartu Keluarga",

                    "Jawaban":
                        "Jawaban kandidat pertama."

                },

                "final_score":
                    0.60

            },

            {

                "row": {

                    "ID":
                        "FAQ002",

                    "Kategori":
                        "Prosedur perubahan data Kartu Keluarga",

                    "Jawaban":
                        "Jawaban kandidat kedua."

                },

                "final_score":
                    0.55

            }

        ]

    }


    response = simulate_conversation(
        result
    )


    passed = True


    passed &= check(
        "success = True",
        response["success"] is True
    )


    passed &= check(
        "method = confidence_medium",
        response["method"]
        == "confidence_medium"
    )


    passed &= check(
        "2 kandidat tersedia",
        len(response["candidates"]) == 2
    )


    passed &= check(
        "kandidat pertama benar",
        response["candidates"][0]["ID"]
        == "FAQ001"
    )


    passed &= check(
        "kandidat kedua benar",
        response["candidates"][1]["ID"]
        == "FAQ002"
    )


    passed &= check(
        "pilihan nomor 1 muncul",
        "1. Persyaratan pembuatan Kartu Keluarga?"
        in response["text"]
    )


    passed &= check(
        "pilihan nomor 2 muncul",
        "2. Prosedur perubahan data Kartu Keluarga?"
        in response["text"]
    )


    passed &= check(
        "opsi 0 muncul",
        "ketik 0"
        in response["text"].lower()
    )


    return passed


# ==================================================
# TEST LOW
# ==================================================

def test_low():

    print()
    print("=" * 60)
    print("TEST LOW")
    print("=" * 60)


    result = {

        "confidence": {

            "level":
                "LOW",

            "score":
                0.25

        },

        "row": {

            "ID":
                "FAQ999",

            "Kategori":
                "",

            "Jawaban":
                ""

        }

    }


    response = simulate_conversation(
        result
    )


    passed = True


    passed &= check(
        "success = False",
        response["success"] is False
    )


    passed &= check(
        "method = confidence_low",
        response["method"]
        == "confidence_low"
    )


    passed &= check(
        "mengarahkan ke Pengaduan",
        "Pengaduan"
        in response["text"]
    )


    passed &= check(
        "tidak ada kandidat",
        len(response["candidates"]) == 0
    )


    return passed


# ==================================================
# TEST MEDIUM TANPA 2 KANDIDAT
# ==================================================

def test_medium_without_candidates():

    print()
    print("=" * 60)
    print("TEST MEDIUM TANPA 2 KANDIDAT")
    print("=" * 60)


    result = {

        "confidence": {

            "level":
                "MEDIUM",

            "score":
                0.50

        },

        "candidates": [

            {

                "row": {

                    "ID":
                        "FAQ001",

                    "Kategori":
                        "Persyaratan KK",

                    "Jawaban":
                        "Jawaban."

                }

            }

        ]

    }


    response = simulate_conversation(
        result
    )


    passed = True


    passed &= check(
        "success = False",
        response["success"] is False
    )


    passed &= check(
        "method = confidence_medium",
        response["method"]
        == "confidence_medium"
    )


    passed &= check(
        "meminta penjelasan kembali",
        "jelaskan kembali"
        in response["text"].lower()
    )


    return passed


# ==================================================
# MAIN TEST RUNNER
# ==================================================

def main():

    print()
    print("=" * 60)
    print("TERATAI AI")
    print("OFFLINE CONFIDENCE FLOW TEST")
    print("=" * 60)


    results = []


    results.append(
        test_high()
    )


    results.append(
        test_medium()
    )


    results.append(
        test_low()
    )


    results.append(
        test_medium_without_candidates()
    )


    print()
    print("=" * 60)
    print("HASIL AKHIR")
    print("=" * 60)


    total = len(
        results
    )


    passed = sum(
        results
    )


    failed = total - passed


    print(
        f"Total : {total}"
    )


    print(
        f"PASS  : {passed}"
    )


    print(
        f"FAIL  : {failed}"
    )


    print("=" * 60)


    if failed == 0:

        print(
            "STATUS : SEMUA TEST BERHASIL"
        )

        print("=" * 60)

        return 0


    print(
        "STATUS : ADA TEST YANG GAGAL"
    )

    print("=" * 60)

    return 1


# ==================================================
# ENTRY POINT
# ==================================================

if __name__ == "__main__":

    exit(
        main()
    )