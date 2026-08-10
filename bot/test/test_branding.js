const brandingService =

    require(

        "../services/brandingService"

    );


console.log(

    "\n========================================"

);

console.log(

    "        TEST BRANDING SERVICE"

);

console.log(

    "========================================\n"

);


try {


    // ======================================
    // AMBIL BRANDING
    // ======================================

    const branding =

        brandingService.getBranding();


    console.log(

        "NAMA KABUPATEN :",

        branding.namaKabupaten

    );


    console.log(

        "NAMA INSTANSI  :",

        branding.namaInstansi

    );


    console.log(

        "NAMA APLIKASI  :",

        branding.namaAplikasi

    );


    console.log(

        "SUBJUDUL       :",

        branding.subjudulAplikasi

    );


    console.log(

        "ALAMAT         :",

        branding.alamat

    );


    console.log(

        "WEBSITE        :",

        branding.website

    );


    console.log(

        "TELEPON        :",

        branding.telepon

    );


    console.log(

        "EMAIL          :",

        branding.email

    );


    console.log(

        "LOGO PATH      :",

        branding.logoPath

    );


    // ======================================
    // VALIDASI
    // ======================================

    const validation =

        brandingService.validateBranding();


    console.log(

        "\n========================================"

    );


    console.log(

        "VALIDASI BRANDING"

    );


    console.log(

        "========================================"

    );


    console.log(

        "STATUS          :",

        validation.valid

            ? "VALID"

            : "TIDAK VALID"

    );


    console.log(

        "LOGO DITEMUKAN  :",

        validation.logoExists

            ? "YA"

            : "TIDAK"

    );


    if (

        validation.missingFields.length > 0

    ) {


        console.log(

            "DATA KURANG     :",

            validation.missingFields

        );

    }


    console.log(

        "\n========================================"

    );


    console.log(

        "TEST BRANDING SELESAI"

    );


    console.log(

        "========================================\n"

    );


}


catch (error) {


    console.error(

        "\nERROR TEST BRANDING:"

    );


    console.error(

        error.message

    );


}