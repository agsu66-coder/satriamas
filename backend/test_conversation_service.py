from services.conversation_service import conversation_service


questions = [

    "Bagaimana cara membuat KTP baru?",

    "Saya ingin membuat KTP",

    "Mengurus kartu keluarga",

    "Saya kehilangan dompet"

]


for q in questions:

    print("=" * 60)

    print(q)

    response = conversation_service.reply(q)

    print(response.to_dict())