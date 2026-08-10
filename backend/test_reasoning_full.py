from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.keyword_service import keyword_service
from services.boundary_service import boundary_service
from services.reasoning_service import reasoning_service



# ==========================================
# LOAD ENGINE
# ==========================================

knowledge_service.load()

semantic_service.load()

keyword_service.load()

boundary_service.load()



# ==========================================
# TEST DATASET
# ==========================================

TEST_CASES = [

    # ======================
    # KTP HILANG
    # ======================

    {
        "query":
            "KTP saya hilang",

        "expected":
            "FAQ-005"
    },

    {
        "query":
            "e ktp saya tidak ada",

        "expected":
            "FAQ-005"
    },

    {
        "query":
            "mau cetak ulang KTP karena hilang",

        "expected":
            "FAQ-005"
    },


    # ======================
    # KTP RUSAK
    # ======================

    {
        "query":
            "KTP saya rusak",

        "expected":
            "FAQ-004"
    },

    {
        "query":
            "chip KTP tidak terbaca",

        "expected":
            "FAQ-004"
    },

    {
        "query":
            "KTP pecah mau diganti",

        "expected":
            "FAQ-004"
    },


    # ======================
    # PINDAH PENDUDUK
    # ======================

    {
        "query":
            "Saya pindah ke Cilacap",

        "expected":
            "FAQ-007"
    },


    {
        "query":
            "Saya pindah keluar Cilacap",

        "expected":
            "FAQ-008"
    },


    {
        "query":
            "Mau pindah domisili",

        "expected":
            "FAQ-007"
    },


    # ======================
    # AKTA KELAHIRAN
    # ======================

    {
        "query":
            "Saya mau membuat akta kelahiran",

        "expected":
            "FAQ-011"
    },


    {
        "query":
            "Cara mengurus akta lahir",

        "expected":
            "FAQ-011"
    },


    # ======================
    # AKTA CERAI
    # ======================

    {
        "query":
            "Saya mau membuat akta cerai",

        "expected":
            "FAQ-017"
    },


    {
        "query":
            "Cara catat perceraian",

        "expected":
            "FAQ-017"
    },


    {
        "query":
            "Cerai non muslim",

        "expected":
            "FAQ-017"
    },


    # ======================
    # PERNIKAHAN
    # ======================

    {
        "query":
            "Saya mau menikah non muslim",

        "expected":
            "FAQ-018"
    },


    {
        "query":
            "Pencatatan perkawinan non muslim",

        "expected":
            "FAQ-018"
    },


    # ======================
    # DATA KEPENDUDUKAN
    # ======================

    {
        "query":
            "Data kependudukan saya tidak ditemukan",

        "expected":
            "FAQ-025"
    },


    {
        "query":
            "NIK saya tidak terdaftar",

        "expected":
            "FAQ-025"
    },


    # ======================
    # KK
    # ======================

    {
        "query":
            "Saya mau cek data KK",

        "expected":
            "FAQ-028"
    },


    # ======================
    # INFORMASI PROSES
    # ======================

    {
        "query":
            "Berapa lama proses dokumen",

        "expected":
            "FAQ-031"
    }

]



# ==========================================
# RUN TEST
# ==========================================


print("="*60)

print(
    "TERATAI AI - FULL REASONING TEST"
)

print("="*60)



total = len(TEST_CASES)

passed = 0



failed_cases = []



for case in TEST_CASES:


    query = case["query"]

    expected = case["expected"]



    result = reasoning_service.search(
        query
    )


    if result:

        actual = result["faq_id"]

        score = result["final_score"]


    else:

        actual = None

        score = 0



    status = (

        "PASS"

        if actual == expected

        else

        "FAIL"

    )



    if status == "PASS":

        passed += 1


    else:

        failed_cases.append({

            "query":
                query,

            "expected":
                expected,

            "actual":
                actual

        })



    print()

    print(
        "QUERY:",
        query
    )

    print(
        "RESULT:",
        actual
    )

    print(
        "EXPECTED:",
        expected
    )

    print(
        "SCORE:",
        score
    )

    print(
        "STATUS:",
        status
    )



print()

print("="*60)

print(
    "AKURASI:",
    passed,
    "/",
    total
)


print(
    "PERSENTASE:",
    round(
        passed / total * 100,
        2
    ),
    "%"
)


print("="*60)



if failed_cases:


    print()

    print(
        "FAILED CASE"
    )

    print("="*60)



    for item in failed_cases:

        print()

        print(
            item["query"]
        )

        print(
            "EXPECTED:",
            item["expected"]
        )

        print(
            "ACTUAL:",
            item["actual"]
        )