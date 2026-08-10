from services.knowledge_service import (
    knowledge_service
)

from services.semantic_service import (
    semantic_service
)

print("=" * 40)
print("KNOWLEDGE")

knowledge_service.load()

print("OK")

print("=" * 40)
print("SEMANTIC")

semantic_service.load()

print("READY :", semantic_service.ready())

print("TOTAL :", semantic_service.total())

print("STAT :", semantic_service.statistics())