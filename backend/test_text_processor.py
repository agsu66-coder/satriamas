from services.text_processor import text_processor

print("=" * 40)
print("TEST TEXT PROCESSOR")
print("=" * 40)

samples = [

    "Saya Mau Membuat KTP",

    "   E-KTP    Baru ",

    "Bagaimana cara bikin KK???",

    "SKTM!!!",

    "PBB 2025"

]

for text in samples:

    print()

    print("INPUT  :", text)

    print("OUTPUT :", text_processor.preprocess(text))