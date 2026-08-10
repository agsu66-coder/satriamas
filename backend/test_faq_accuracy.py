from services.semantic_service import semantic_service
from services.knowledge_service import knowledge_service
from services.excel_service import excel_service


def load_test_data():

    rows = excel_service.read_as_dict(
        "TEST"
    )

    return rows



def run_test():

    print("=" * 50)
    print("TERATAI FAQ ACCURACY TEST")
    print("=" * 50)


    knowledge_service.load()

    semantic_service.load()


    tests = load_test_data()


    total = 0
    correct = 0


    for item in tests:

        total += 1


        question = item.get(
            "Pertanyaan",
            ""
        )


        expected = str(
            item.get(
                "Expected_FAQ_ID",
                ""
            )
        ).strip()



        result = semantic_service.search(
            question
        )


        if result:

            found = str(
                result["row"].get(
                    "ID",
                    ""
                )
            ).strip()


            score = result["score"]


        else:

            found = "NOT_FOUND"

            score = 0



        if found == expected:

            correct += 1

            status = "BENAR"


        else:

            status = "SALAH"



        print()

        print(
            f"Pertanyaan : {question}"
        )

        print(
            f"Target     : {expected}"
        )

        print(
            f"Hasil      : {found}"
        )

        print(
            f"Score      : {score:.4f}"
        )

        print(
            f"Status     : {status}"
        )



    accuracy = (

        correct / total * 100

        if total > 0

        else 0

    )


    print()

    print("=" * 50)

    print(
        f"Akurasi : {accuracy:.2f}%"
    )

    print("=" * 50)



if __name__ == "__main__":

    run_test()