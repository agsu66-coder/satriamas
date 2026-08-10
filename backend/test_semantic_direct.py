from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service


print("="*50)
print("LOAD KNOWLEDGE")

knowledge_service.load()


print(
    "TRAINING:",
    knowledge_service.total()
)


print("="*50)
print("LOAD SEMANTIC")


semantic_service.load()


print(
    "SEMANTIC TOTAL:",
    semantic_service.total()
)


query = "KTP saya hilang mau cetak baru"


print("="*50)
print("QUERY:")
print(query)


results = semantic_service.search_candidates(
    query,
    limit=10
)


for item in results:

    print()

    print(
        item["row"]["ID"]
    )

    print(
        item["score"]
    )

    print(
        item["row"]["Kategori"]
    )