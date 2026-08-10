const messageHandler =
    require("../../bot/handlers/messageHandler");

const stateService =
    require("../../bot/services/stateService");

const aduanService =
    require("../../bot/services/aduanService");


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


// =====================================
// MOCK MESSAGE
// =====================================

function createMsg({

    from,

    notifyName,

    body,

    hasQuotedMsg = false,

    quotedText = ""

}) {

    return {

        from,

        body,

        fromMe: false,

        isStatus: false,

        hasQuotedMsg,

        _data: {

            notifyName,

            quotedMsg: hasQuotedMsg

                ? {

                    body: quotedText

                }

                : null

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


// =====================================
// DATA TEST
// =====================================

const WARGA =
    "6287736833184@c.us";

const PETUGAS =
    "6282227026480@c.us";


// =====================================
// FUNGSI TEST
// =====================================

async function runTest() {

    console.log("\n================================");

    console.log(
        "TEST MESSAGE HANDLER - MULTIPLE COMPLAINTS"
    );

    console.log("================================");


    // =====================================
    // TEST 1
    // BUAT ADUAN PERTAMA
    // =====================================

    console.log(
        "\n=== TEST 1 : BUAT ADUAN PERTAMA ==="
    );


    const aduan1 =
        aduanService.create({

            No_WA:
                WARGA,

            Nama:
                "Guz Memed",

            Kategori_ID:
                "KAT001",

            Isi:
                "Aduan pertama",

            Owner:
                "PTG001"

        });


    aduanService.updateStatus(

        aduan1,

        "MENUNGGU_INFO"

    );


    aduanService.increaseInfoCount(

        aduan1

    );


    aduanService.addInfoHistory(

        aduan1,

        "Mohon informasi tambahan untuk aduan pertama."

    );


    console.log(
        "ADUAN 1 :",
        aduan1
    );


    // =====================================
    // TEST 2
    // BUAT ADUAN KEDUA
    // =====================================

    console.log(
        "\n=== TEST 2 : BUAT ADUAN KEDUA ==="
    );


    const aduan2 =
        aduanService.create({

            No_WA:
                WARGA,

            Nama:
                "Guz Memed",

            Kategori_ID:
                "KAT001",

            Isi:
                "Aduan kedua",

            Owner:
                "PTG001"

        });


    aduanService.updateStatus(

        aduan2,

        "MENUNGGU_INFO"

    );


    aduanService.increaseInfoCount(

        aduan2

    );


    aduanService.addInfoHistory(

        aduan2,

        "Mohon informasi tambahan untuk aduan kedua."

    );


    console.log(
        "ADUAN 2 :",
        aduan2
    );


    // =====================================
    // TEST 3
    // WARGA MENJAWAB ADUAN PERTAMA
    // =====================================

    console.log(
        "\n=== TEST 3 : JAWAB ADUAN PERTAMA ==="
    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                WARGA,

            notifyName:
                "Guz Memed",

            body:
                "Ini jawaban untuk aduan pertama.",

            hasQuotedMsg:
                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${aduan1}

Petugas meminta informasi berikut:

Mohon informasi tambahan untuk aduan pertama.

Silakan balas pesan ini.`

        })

    );


    // =====================================
    // TEST 4
    // WARGA MENJAWAB ADUAN KEDUA
    // =====================================

    console.log(
        "\n=== TEST 4 : JAWAB ADUAN KEDUA ==="
    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                WARGA,

            notifyName:
                "Guz Memed",

            body:
                "Ini jawaban untuk aduan kedua.",

            hasQuotedMsg:
                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${aduan2}

Petugas meminta informasi berikut:

Mohon informasi tambahan untuk aduan kedua.

Silakan balas pesan ini.`

        })

    );


    // =====================================
    // VERIFIKASI
    // =====================================

    console.log(
        "\n=== VERIFIKASI MULTIPLE COMPLAINTS ==="
    );


    const hasil1 =
        aduanService.getById(

            aduan1

        );


    const hasil2 =
        aduanService.getById(

            aduan2

        );


    console.log(
        "\nADUAN 1:"
    );

    console.log({

        ID:
            hasil1.ID,

        Status:
            hasil1.Status,

        Riwayat_Info:
            hasil1.Riwayat_Info

    });


    console.log(
        "\nADUAN 2:"
    );

    console.log({

        ID:
            hasil2.ID,

        Status:
            hasil2.Status,

        Riwayat_Info:
            hasil2.Riwayat_Info

    });


    console.log(
        "\n================================"
    );

    console.log(
        "TEST MULTIPLE COMPLAINTS SELESAI"
    );

    console.log(
        "================================"
    );

}


// =====================================
// JALANKAN TEST
// =====================================

runTest()

    .catch(err => {

        console.error(

            "TEST MULTIPLE COMPLAINTS ERROR:",

            err

        );

    });