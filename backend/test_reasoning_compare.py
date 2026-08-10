"""
==================================================
TERATAI AI

Reasoning Engine Compare Test

Membandingkan:

1. KnowledgeEngine Lama
2. ReasoningService Baru

==================================================
"""


from services.knowledge_engine import knowledge_engine
from services.reasoning_service import reasoning_service


# ==============================================
# INIT
# ==============================================

print("="*60)
print("TERATAI AI REASONING COMPARE TEST")
print("="*60)


knowledge_engine.load()


queries = [

    "KTP saya hilang",

    "Saya mau membuat akta cerai",

    "Saya mau cek data KK",

    "berapa lama membuat dokumen",

    "cara mengurus kartu keluarga",

    "berapa harga motor bekas"

]


# ==============================================
# TEST
# ==============================================


for query in queries:


    print("\n")
    print("="*60)

    print("QUERY:")
    print(query)


    # ==========================================
    # OLD ENGINE
    # ==========================================

    print("\n--- OLD KNOWLEDGE ENGINE ---")


    old_result = knowledge_engine.search(
        query
    )


    print(
        old_result.to_dict()
    )



    # ==========================================
    # NEW REASONING
    # ==========================================


    print("\n--- NEW REASONING ENGINE ---")


    new_result = reasoning_service.search(
        query
    )


    if new_result:


        print({

            "faq_id":
                new_result["faq_id"],

            "semantic":
                new_result["semantic_score"],

            "keyword":
                new_result["keyword_score"],

            "boundary":
                new_result["boundary_score"],

            "final":
                new_result["final_score"],

            "confidence":
                new_result["confidence"]

        })


    else:


        print(
            "NOT FOUND"
        )
