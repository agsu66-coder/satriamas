from services.knowledge_service import knowledge_service


knowledge_service.load()


data = knowledge_service.get_training_data()


print("="*50)

print(
    "TOTAL TRAINING:",
    len(data)
)


for item in data:

    if item["key"] in [
        "FAQ-016",
        "FAQ-017",
        "FAQ-018"
    ]:

        print()
        print(item["key"])
        print(item["text"])