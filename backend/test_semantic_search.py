from services.knowledge_service import knowledge_service
from services.semantic_service import semantic_service

knowledge_service.load()
semantic_service.load()

queries = [

    "Bagaimana cara membuat KTP baru?",

    "Saya ingin membuat KTP",

    "Cara bikin e KTP",

    "Mengurus kartu keluarga",

    "Saya ingin melapor pelayanan",

    "Saya kehilangan dompet"

]

for q in queries:

    print("=" * 60)

    print(q)

    result = semantic_service.search(q)

    print(result)