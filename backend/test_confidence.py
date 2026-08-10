from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service
from services.keyword_service import keyword_service
from services.boundary_service import boundary_service
from services.reasoning_service import reasoning_service



knowledge_service.load()

semantic_service.load()

keyword_service.load()

boundary_service.load()



tests = [

    "KTP saya hilang",

    "Saya mau membuat akta cerai",

    "Saya mau cek data KK",

    "berapa harga motor bekas"

]



print("="*60)

print("TERATAI AI CONFIDENCE TEST")

print("="*60)



for query in tests:


    print("\nQUERY:")

    print(query)


    result = reasoning_service.search(query)


    print("\nRESULT:")


    print(result)