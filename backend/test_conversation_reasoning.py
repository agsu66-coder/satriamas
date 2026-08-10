from services.conversation_service import (
    conversation_service
)


tests = [

    "KTP saya hilang",

    "Saya mau membuat akta cerai",

    "Saya mau cek data KK",

    "berapa harga motor bekas"

]


print("="*60)
print("TERATAI CONVERSATION REASONING TEST")
print("="*60)


for q in tests:


    print("\nQUERY:")
    print(q)


    response = conversation_service.reply(
        q
    )


    print(
        response.to_dict()
    )