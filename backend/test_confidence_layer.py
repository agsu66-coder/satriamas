from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.keyword_service import keyword_service
from services.boundary_service import boundary_service
from services.reasoning_service import reasoning_service


knowledge_service.load()
semantic_service.load()
keyword_service.load()
boundary_service.load()



queries = [

    "KTP saya hilang",

    "Saya mau membuat akta cerai",

    "berapa harga motor bekas"

]



print("="*60)
print("TERATAI AI CONFIDENCE LAYER TEST")
print("="*60)



for query in queries:


    print("\nQUERY:")
    print(query)


    result = reasoning_service.search(query)



    if result:


        print(
            "FAQ:",
            result["faq_id"]
        )


        print(
            "FINAL:",
            result["final_score"]
        )


        print(
            "CONFIDENCE:",
            result["confidence"]
        )


    else:

        print(
            "NO RESULT"
        )