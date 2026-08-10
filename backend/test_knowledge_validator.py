from services.knowledge_validator import KnowledgeValidator


faq = {

    "ID":"KTP001",

    "Kategori":
    "Administrasi Kependudukan",

    "Keyword":
    "ktp hilang;kehilangan ktp",

    "Variasi_1":
    "ktp saya hilang",

    "Variasi_2":
    "ktp ilang",

    "Variasi_3":
    "ktp tidak ada",

    "Jawaban":
    "Silakan membuat surat kehilangan."

}


validator = KnowledgeValidator()


result = validator.validate(
    faq
)


print(result)