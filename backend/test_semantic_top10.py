from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service


knowledge_service.load()
semantic_service.load()


query = "Saya mau membuat akta cerai"


embedding = semantic_service._encode_query(query)


index_scores = semantic_service._best_match(
    embedding
)


scores = semantic_service.embeddings


from sentence_transformers import util


result = util.cos_sim(
    embedding,
    scores
)[0]


ranking = sorted(
    enumerate(result.tolist()),
    key=lambda x:x[1],
    reverse=True
)


for index, score in ranking[:10]:

    item = semantic_service.training_data[index]

    print(
        item["key"],
        score,
        item["text"]
    )