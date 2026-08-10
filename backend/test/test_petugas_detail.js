const petugasAduanDetailHandler =
    require("../../bot/handlers/petugasAduanDetailHandler");


// =====================================
// SIMULASI PESAN WHATSAPP
// =====================================

function createMessage(namaWA, body) {

    return {

        _data: {

            notifyName: namaWA

        },

        body,

        reply: async function (text) {

            console.log("\n===== BALASAN BOT =====");

            console.log(text);

            console.log("=======================\n");

        }

    };

}


// =====================================
// SIMULASI CLIENT
// =====================================

const client = {};


// =====================================
// TEST
// =====================================

async function test() {

    const namaWA = "Rose";

    const aduanId =
        "ADU-20260718-0002";


    console.log(
        "================================"
    );

    console.log(
        "TEST DETAIL ADUAN PETUGAS"
    );

    console.log(
        "PETUGAS :",
        namaWA
    );

    console.log(
        "================================"
    );


    // =================================
    // TEST 1
    // =================================

    console.log(
        "\n=== TEST 1 : ID ADUAN VALID ==="
    );


    /*
     * Catatan:
     *
     * Handler membutuhkan session:
     *
     * {
     *
     *     mode: "DETAIL_ADUAN",
     *
     *     ownerId: "PTG001"
     *
     * }
     *
     * Session tersebut harus dibuat
     * sebelum handler dijalankan.
     */


    const conversationService =
        require("../../bot/services/conversationService");


    conversationService.set(

        namaWA,

        {

            mode: "DETAIL_ADUAN",

            ownerId: "PTG001"

        }

    );


    await petugasAduanDetailHandler.processDetail(

        client,

        createMessage(

            namaWA,

            aduanId

        )

    );


    // =================================
    // TEST 2
    // =================================

    console.log(
        "\n=== TEST 2 : ID ADUAN TIDAK VALID ==="
    );


    conversationService.set(

        namaWA,

        {

            mode: "DETAIL_ADUAN",

            ownerId: "PTG001"

        }

    );


    await petugasAduanDetailHandler.processDetail(

        client,

        createMessage(

            namaWA,

            "ADU-TIDAK-ADA"

        )

    );


    // =================================
    // TEST 3
    // =================================

    console.log(
        "\n=== TEST 3 : ADUAN MILIK PETUGAS LAIN ==="
    );


    conversationService.set(

        namaWA,

        {

            mode: "DETAIL_ADUAN",

            ownerId: "PTG999"

        }

    );


    await petugasAduanDetailHandler.processDetail(

        client,

        createMessage(

            namaWA,

            aduanId

        )

    );


    // =================================
    // TEST 4
    // =================================

    console.log(
        "\n=== TEST 4 : KEMBALI ==="
    );


    conversationService.set(

        namaWA,

        {

            mode: "DETAIL_ADUAN",

            ownerId: "PTG001"

        }

    );


    await petugasAduanDetailHandler.processDetail(

        client,

        createMessage(

            namaWA,

            "0"

        )

    );


    // =================================
    // TEST 5
    // =================================

    console.log(
        "\n=== TEST 5 : TANPA SESSION ==="
    );


    conversationService.clear(

        namaWA

    );


    const hasil =

        await petugasAduanDetailHandler.processDetail(

            client,

            createMessage(

                namaWA,

                aduanId

            )

        );


    console.log(

        "HASIL :",

        hasil

    );

}


test();