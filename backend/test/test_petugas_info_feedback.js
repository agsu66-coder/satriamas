const petugasService =
    require("../../bot/services/petugasService");

const conversationService =
    require("../../bot/services/conversationService");

const petugasHandler =
    require("../../bot/handlers/petugasHandler");

const aduanService =
    require("../../bot/services/aduanService");

const petugas =
    petugasService.getByName("Rose");

const ADUAN_ID =
    "ADU-20260718-0002";

console.log("=== DATA PETUGAS ===");
console.log(petugas);
console.log("====================");

// =====================================
// MOCK CLIENT
// =====================================
    const mockClient = {

        async sendMessage(to, text) {

            console.log("\n===== MOCK SEND MESSAGE =====");

            console.log("KEPADA :", to);

            console.log("PESAN :");

            console.log(text);

            console.log("=============================\n");

        }

   };



function createMsg(body) {

    return {

        body,

        from: "6282227026480@c.us",

        _data: {

            notifyName: "Rose"

        },

        hasQuotedMsg: false,

        replies: [],

        async reply(text) {

            console.log("\n===== BALASAN BOT =====");
            console.log(text);
            console.log("=======================\n");

            this.replies.push(text);

        }

    };

}

async function runTest() {

    console.log("================================");
    console.log("TEST INFO DAN FEEDBACK PETUGAS");
    console.log("PETUGAS :", petugas.Nama_WA);
    console.log("ADUAN   :", ADUAN_ID);
    console.log("================================");


    // =================================
    // TEST 1 : SESSION INFO
    // =================================

    console.log("\n=== TEST 1 : SESSION INFO ===");

    conversationService.set(

        petugas.Nama_WA,

        {

            mode: "INFO",

            aduanId: ADUAN_ID

        }

    );

    const msg1 =
        createMsg(

            "Mohon lampirkan dokumen pendukung."

        );

    const hasil1 =
        await petugasHandler.handlePetugas(

            mockClient,

            msg1

        );

    console.log("HASIL :", hasil1);

    console.log(

        "SESSION :",

        conversationService.get(

            petugas.Nama_WA

        )

    );

    console.log(

        "ADUAN :",

        aduanService.getById(

            ADUAN_ID

        )

    );


    // =================================
    // TEST 2 : SESSION FEEDBACK
    // =================================

    console.log("\n=== TEST 2 : SESSION FEEDBACK ===");

    conversationService.set(

        petugas.Nama_WA,

        {

            mode: "FEEDBACK",

            aduanId: ADUAN_ID

        }

    );

    const msg2 =
        createMsg(

            "Permohonan telah ditindaklanjuti oleh petugas."

        );

    const hasil2 =
        await petugasHandler.handlePetugas(

            mockClient,

            msg2

        );

    console.log("HASIL :", hasil2);

    console.log(

        "SESSION :",

        conversationService.get(

            petugas.Nama_WA

        )

    );

    console.log(

        "ADUAN :",

        aduanService.getById(

            ADUAN_ID

        )

    );


    console.log("\n================================");
    console.log("TEST SELESAI");
    console.log("================================");

}
runTest();