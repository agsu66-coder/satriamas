from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.knowledge_conflict import knowledge_conflict



knowledge_service.load()

semantic_service.load()



result = knowledge_conflict.analyze(
    semantic_service.embeddings,
    threshold=0.70
)



print("="*50)

print(
    "TOTAL CONFLICT:",
    len(result)
)


for item in result:

    print()

    print(
        item
    )