from models.ai_response import AIResponse


response = AIResponse(

    success=True,

    text="Halo, selamat datang.",

    category="Greeting",

    method="template",

    confidence=1.0

)

print(response)

print()

print(response.to_dict())

print()

print(bool(response))