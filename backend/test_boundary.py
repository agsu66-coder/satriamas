from services.boundary_service import boundary_service


boundary_service.load()


print("="*50)

print(
    "TOTAL BOUNDARY:",
    boundary_service.total()
)


tests = [

    (
        "KTP saya hilang mau cetak baru",
        "FAQ-004"
    ),

    (
        "KTP saya hilang mau cetak baru",
        "FAQ-005"
    ),


    (
        "Saya pindah ke Cilacap",
        "FAQ-007"
    ),


    (
        "Saya pindah keluar Cilacap",
        "FAQ-008"
    )

]


for query, faq in tests:


    result = boundary_service.check(
        query,
        faq
    )


    print()
    print("QUERY :", query)
    print("FAQ   :", faq)
    print(result)