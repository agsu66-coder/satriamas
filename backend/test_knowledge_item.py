from models.knowledge_item import KnowledgeItem


row = {

    "ID": "FAQ001",

    "Kategori": "Administrasi",

    "Keyword": "ktp",

    "Variasi_1": "buat ktp",

    "Variasi_2": "cara membuat ktp",

    "Variasi_3": "bikin ktp",

    "Jawaban": "Silakan datang ke kecamatan.",

    "Sumber": "Disdukcapil",

    "Status": "Aktif",

    "Terakhir_Update": "2026-07-09"

}

item = KnowledgeItem.from_dict(row)

print(item)

print(item.training_text)

print(item.is_active)

print(item.to_dict())