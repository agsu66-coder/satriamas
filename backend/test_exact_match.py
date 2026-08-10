from services.knowledge_engine import knowledge_engine

knowledge_engine.load()

queries = [

    # Exact Match
    "Bagaimana cara membuat KTP baru?",
    "ktp",

    # Keyword Match
    "Saya ingin membuat KTP",
    "Cara bikin e KTP",
    "Mengurus kartu keluarga",
    "Saya ingin melapor pelayanan",
    "Pelayanan kantor kecamatan",

    # Tidak ditemukan
    "Saya kehilangan dompet"
]

for q in queries:

    print("=" * 70)
    print(q)

    result = knowledge_engine.search(q)

    print(result.to_dict())