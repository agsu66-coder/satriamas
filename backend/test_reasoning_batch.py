from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.boundary_service import boundary_service
from services.reasoning_service import reasoning_service
from services.keyword_service import keyword_service


# LOAD ENGINE

knowledge_service.load()

semantic_service.load()

boundary_service.load()

keyword_service.load()


# ======================================
# TEST CASE
# ======================================

tests = [

    {
        "query": "KTP saya hilang",
        "expected": "FAQ-005"
    },

    {
        "query": "KTP saya rusak pecah",
        "expected": "FAQ-004"
    },

    {
        "query": "Saya pindah ke Cilacap",
        "expected": "FAQ-007"
    },

    {
        "query": "Saya pindah keluar Cilacap",
        "expected": "FAQ-008"
    },

    {
        "query": "Saya mau membuat akta kelahiran",
        "expected": "FAQ-011"
    },

    {
        "query": "Saya mau membuat akta cerai",
        "expected": "FAQ-017"
    },

    {
        "query": "Saya mau menikah non muslim",
        "expected": "FAQ-018"
    },

    {
        "query": "Data kependudukan saya tidak ditemukan",
        "expected": "FAQ-025"
    },

    {
        "query": "Saya mau cek data KK",
        "expected": "FAQ-028"
    },

    {
        "query": "Berapa lama proses dokumen",
        "expected": "FAQ-031"
    }

]


# ======================================
# RUN TEST
# ======================================


total = 0
correct = 0


print("="*60)
print("REASONING ENGINE BATCH TEST")
print("="*60)


for test in tests:

    total += 1

    result = reasoning_service.search(
        test["query"]
    )


    print()
    print("QUERY:")
    print(test["query"])


    if result is None:

        print("RESULT : NONE")
        continue


    faq = result["faq_id"]


    print(
        "RESULT :",
        faq
    )


    print(
        "EXPECTED:",
        test["expected"]
    )


    print(
        "SCORE:",
        result["final_score"]
    )


    if faq == test["expected"]:

        print("STATUS : PASS")
        correct += 1

    else:

        print("STATUS : FAIL")


print()
print("="*60)

print(
    "AKURASI:",
    correct,
    "/",
    total
)

print("="*60)