from services.ai_service import ai_service

tests = [

    "Halo",
    "Hai",
    "Terima kasih",
    "Thanks",
    "Dadah",
    "Bagaimana cara membuat KTP baru?",
    "Saya ingin membuat KTP",
    "Mengurus kartu keluarga",
    "Saya kehilangan dompet"

]

for text in tests:

    print("=" * 60)

    print(text)

    result = ai_service.reply(text)

    print(result.to_dict())