from dataclasses import dataclass, field
from typing import List


@dataclass
class KnowledgeItem:
    """
    Representasi satu knowledge/FAQ TERATAI.

    Model ini hanya menyimpan data.
    Tidak memiliki logika bisnis.
    """

    id: str = ""

    category: str = ""

    keyword: str = ""

    variations: List[str] = field(default_factory=list)

    answer: str = ""

    source: str = ""

    status: str = ""

    updated_at: str = ""

    # ======================================

    @classmethod
    def from_dict(cls, data: dict):

        return cls(

            id=str(data.get("ID", "")).strip(),

            category=str(
                data.get("Kategori", "")
            ).strip(),

            keyword=str(
                data.get("Keyword", "")
            ).strip(),

            variations=[

                str(data.get("Variasi_1", "")).strip(),

                str(data.get("Variasi_2", "")).strip(),

                str(data.get("Variasi_3", "")).strip()

            ],

            answer=str(
                data.get("Jawaban", "")
            ).strip(),

            source=str(
                data.get("Sumber", "")
            ).strip(),

            status=str(
                data.get("Status", "")
            ).strip(),

            updated_at=str(
                data.get("Terakhir_Update", "")
            ).strip()

        )

    # ======================================

    def to_dict(self):

        return {

            "ID": self.id,

            "Kategori": self.category,

            "Keyword": self.keyword,

            "Variasi_1": self.variations[0] if len(self.variations) > 0 else "",

            "Variasi_2": self.variations[1] if len(self.variations) > 1 else "",

            "Variasi_3": self.variations[2] if len(self.variations) > 2 else "",

            "Jawaban": self.answer,

            "Sumber": self.source,

            "Status": self.status,

            "Terakhir_Update": self.updated_at

        }

    # ======================================

    @property
    def is_active(self):

        return self.status.lower() == "aktif"

    # ======================================

    @property
    def training_text(self):

        items = []

        if self.keyword:
            items.append(self.keyword)

        for item in self.variations:

            if item:
                items.append(item)

        return " ".join(items)

    # ======================================

    def __str__(self):

        return f"[{self.id}] {self.keyword}"