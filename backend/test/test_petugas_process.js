const petugasService =
    require("../../bot/services/petugasService");

const conversationService =
    require("../../bot/services/conversationService");

const processHandler =
    require("../../bot/handlers/petugasAduanProcessHandler");


const petugas =
    petugasService.getByName("Rose");


const ADUAN_ID =
    "ADU-20260718-0002";


console.log("=== DATA PETUGAS ===");
console.log(petugas);
console.log("====================");


function createMsg(body) {

    return {

        body,

        _data: {

            notifyName: "Rose"

        },

        replies: [],

        async reply(text) {

            console.log("\n===== BALASAN BOT =====");
            console.log(text);
            console.log("=======================\n");

            this.replies.push(text);

        }

    };

}


function setDetailSession() {

    conversationService.set(

        petugas.Nama_WA,

        {

            mode: "ADUAN_DETAIL",

            aduanId: ADUAN_ID

        }

    );

}


async function runTest() {

    console.log("================================");
    console.log("TEST PROSES ADUAN PETUGAS");
    console.log("PETUGAS :", petugas.Nama_WA);
    console.log("================================");


    // =================================
    // TEST 1 : PILIHAN INFORMASI
    // =================================

    console.log(
        "\n=== TEST 1 : PILIHAN 1 - INFORMASI ==="
    );

    setDetailSession();

    const msg1 =
        createMsg("1");

    const hasil1 =
        await processHandler.processAduan(

            null,

            msg1

        );

    console.log("HASIL :", hasil1);

    console.log(
        "SESSION :",
        conversationService.get(

            petugas.Nama_WA

        )

    );


    // =================================
    // TEST 2 : PILIHAN FEEDBACK
    // =================================

    console.log(
        "\n=== TEST 2 : PILIHAN 2 - FEEDBACK ==="
    );

    setDetailSession();

    const msg2 =
        createMsg("2");

    const hasil2 =
        await processHandler.processAduan(

            null,

            msg2

        );

    console.log("HASIL :", hasil2);

    console.log(
        "SESSION :",
        conversationService.get(

            petugas.Nama_WA

        )

    );


    // =================================
    // TEST 3 : KEMBALI
    // =================================

    console.log(
        "\n=== TEST 3 : PILIHAN 0 - KEMBALI ==="
    );

    setDetailSession();

    const msg3 =
        createMsg("0");

    const hasil3 =
        await processHandler.processAduan(

            null,

            msg3

        );

    console.log("HASIL :", hasil3);

    console.log(
        "SESSION :",
        conversationService.get(

            petugas.Nama_WA

        )

    );


    // =================================
    // TEST 4 : SESSION TIDAK ADA
    // =================================

    console.log(
        "\n=== TEST 4 : TANPA SESSION ==="
    );

    conversationService.clear(

        petugas.Nama_WA

    );

    const msg4 =
        createMsg("1");

    const hasil4 =
        await processHandler.processAduan(

            null,

            msg4

        );

    console.log("HASIL :", hasil4);


    console.log("\n================================");
    console.log("TEST SELESAI");
    console.log("================================");

}


runTest();