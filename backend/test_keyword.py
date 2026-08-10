from services.knowledge_service import knowledge_service
from services.keyword_service import keyword_service


knowledge_service.load()

keyword_service.load()


queries = [


    "Saya mau membuat akta cerai"


]


for query in queries:

    print("="*50)

    print(query)


    results = keyword_service.search_candidates(
        query,
        limit=3
    )


    for item in results:

        print(
            item["row"]["ID"],
            item["keyword_score"],
            item["matched_keywords"]
        )