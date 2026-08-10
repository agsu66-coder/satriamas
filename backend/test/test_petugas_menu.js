const petugasMenuHandler =
    require("../../bot/handlers/petugasMenuHandler");


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


    console.log(
        "================================"
    );

    console.log(
        "TEST PETUGAS MENU HANDLER"
    );

    console.log(
        "PETUGAS :",
        namaWA
    );

    console.log(
        "================================"
    );


    // ================================
    // 1. BUKA DASHBOARD
    // ================================

    console.log(
        "\n=== TEST 1 : DASHBOARD ==="
    );

    await petugasMenuHandler.processMenu(

        client,

        createMessage(

            namaWA,

            "DASHBOARD"

        )

    );


    // ================================
    // 2. ADUAN SAYA
    // ================================

    console.log(
        "\n=== TEST 2 : ADUAN SAYA ==="
    );

    await petugasMenuHandler.processMenu(

        client,

        createMessage(

            namaWA,

            "1"

        )

    );


    // ================================
    // 3. ADUAN BARU
    // ================================

    console.log(
        "\n=== TEST 3 : ADUAN BARU ==="
    );

    await petugasMenuHandler.processMenu(

        client,

        createMessage(

            namaWA,

            "2"

        )

    );


    // ================================
    // 4. MENUNGGU INFORMASI
    // ================================

    console.log(
        "\n=== TEST 4 : MENUNGGU INFORMASI ==="
    );

    await petugasMenuHandler.processMenu(

        client,

        createMessage(

            namaWA,

            "3"

        )

    );


    // ================================
    // 5. SEDANG DIPROSES
    // ================================

    console.log(
        "\n=== TEST 5 : DIPROSES ==="
    );

    await petugasMenuHandler.processMenu(

        client,

        createMessage(

            namaWA,

            "4"

        )

    );


    // ================================
    // 6. RIWAYAT SELESAI
    // ================================

    console.log(
        "\n=== TEST 6 : SELESAI ==="
    );

    await petugasMenuHandler.processMenu(

        client,

        createMessage(

            namaWA,

            "5"

        )

    );


    // ================================
    // 7. KELUAR
    // ================================

    console.log(
        "\n=== TEST 7 : KELUAR ==="
    );

    await petugasMenuHandler.processMenu(

        client,

        createMessage(

            namaWA,

            "0"

        )

    );


    // ================================
    // 8. BUKAN PETUGAS
    // ================================

    console.log(
        "\n=== TEST 8 : BUKAN PETUGAS ==="
    );

    const hasil =

        await petugasMenuHandler.processMenu(

            client,

            createMessage(

                "Nomor Tidak Terdaftar",

                "DASHBOARD"

            )

        );


    console.log(

        "HASIL :",

        hasil

    );

}


test();