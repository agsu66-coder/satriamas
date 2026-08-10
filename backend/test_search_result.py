from models.knowledge_item import KnowledgeItem
from models.search_result import SearchResult


item = KnowledgeItem(

    id="FAQ001",

    category="Administrasi",

    keyword="ktp",

    answer="Silakan datang ke Kecamatan."

)

result = SearchResult(

    found=True,

    method="keyword",

    score=0.94,

    knowledge=item,

    matched_text="buat ktp",

    processing_time=4.25

)

print(result)

print(result.answer)

print(result.category)

print(result.knowledge_id)

print(result.to_dict())

print(bool(result))