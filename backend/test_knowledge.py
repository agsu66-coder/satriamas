from services.knowledge_service import knowledge_service

print("=" * 40)
print("TEST KNOWLEDGE SERVICE")
print("=" * 40)

print("\nLOAD")

knowledge_service.load()

print("OK")

print("\nSTATISTICS")

print(
    knowledge_service.statistics()
)

print("\nTOTAL")

print(
    knowledge_service.total()
)

print("\nTRAINING")

print(
    len(
        knowledge_service.get_training_data()
    )
)

print("\nEXISTS")

print(
    knowledge_service.exists(
        "FAQ002"
    )
)

print("\nFIND")

print(
    knowledge_service.find_by_key(
        "FAQ001"
    )
)

print("\nFIRST TRAINING")

training = knowledge_service.get_training_data()

if training:

    print(training[0])

print("=" * 40)

print("\nFAQ000002")

row = knowledge_service.find_by_key("FAQ000002")

print(row)