from services.knowledge_engine import knowledge_engine

knowledge_engine.load()

queries = [

    "bagaimana mengurus identitas penduduk",

    "saya mau membuat kartu identitas",

    "ingin bikin kartu tanda penduduk",

    "lapor pelayanan",

    "saya kehilangan dompet"

]

for q in queries:

    print("=" * 60)

    print(q)

    result = knowledge_engine.search(q)

    print(result.to_dict())