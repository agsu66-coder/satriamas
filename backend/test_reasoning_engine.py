from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.boundary_service import boundary_service
from services.reasoning_service import reasoning_service


knowledge_service.load()

semantic_service.load()

boundary_service.load()


query = "KTP saya hilang mau cetak baru"


result = reasoning_service.search(query)


print("="*50)

print("QUERY:")
print(query)


print("\nRESULT")


if result:


    print(
        "FAQ:",
        result["faq_id"]
    )


    print(
        "semantic:",
        result["semantic_score"]
    )


    print(
        "boundary:",
        result["boundary"]
    )


    print(
        "FINAL:",
        result["final_score"]
    )


else:

    print(
        "Tidak ada hasil reasoning"
    )