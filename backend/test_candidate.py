from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.boundary_service import boundary_service


knowledge_service.load()

semantic_service.load()

boundary_service.load()


query = "Saya mau membuat akta cerai"


results = semantic_service.search_candidates(
    query,
    limit=10
)


print("="*50)
print("QUERY:")
print(query)

print("="*50)

for item in results:

    print(
        item["row"]["ID"],
        item["score"],
        item["row"]["Kategori"]
    )