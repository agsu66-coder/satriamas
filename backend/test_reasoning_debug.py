from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.keyword_service import keyword_service
from services.boundary_service import boundary_service
from services.reasoning_service import reasoning_service


knowledge_service.load()
semantic_service.load()
keyword_service.load()
boundary_service.load()


query = "Saya mau membuat akta cerai"


print("="*50)

print("SEMANTIC")


for x in semantic_service.search_candidates(query,10):

    print(
        x["row"]["ID"],
        x.get("score",0)
    )



print("="*50)

print("KEYWORD")


for x in keyword_service.search_candidates(query,10):

    print(
        x["row"]["ID"],
        x.get("keyword_score",0),
        x.get("matched_keywords",[])
    )



print("="*50)

print("REASONING")


result = reasoning_service.search(query)


print(result)