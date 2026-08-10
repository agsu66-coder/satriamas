from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service

knowledge_service.load()
semantic_service.load()

query = "Bagaimana cara membuat KTP baru?"

embedding = semantic_service._encode_query(query)

print("EMBEDDING")
print(embedding is not None)

index, score = semantic_service._best_match(
    embedding
)

print("INDEX :", index)
print("SCORE :", score)

training = semantic_service.training_data[index]

print("CATEGORY :", training["category"])
print("KEY :", training["key"])