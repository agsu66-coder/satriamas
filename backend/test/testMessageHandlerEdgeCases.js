const messageHandler =
    require("../../bot/handlers/messageHandler");

const conversationService =
    require("../../bot/services/conversationService");

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
// DATA
// =====================================

const WARGA =
    "6287736833184@c.us";

const PETUGAS =
    "6282227026480@c.us";

const NAMA_PETUGAS =
    "Rose";


// =====================================
// BUAT ADUAN KHUSUS EDGE TEST
// =====================================

const ADUAN_EDGE =
    aduanService.create({

        No_WA:
            WARGA,

        Nama:
            "Guz Memed",

        Kategori_ID:
            "KAT001",

        Isi:
            "Aduan khusus pengujian edge case",

        Owner:
            "PTG001"

    });


aduanService.updateStatus(

    ADUAN_EDGE,

    "MENUNGGU_INFO"

);


aduanService.increaseInfoCount(

    ADUAN_EDGE

);


aduanService.addInfoHistory(

    ADUAN_EDGE,

    "Mohon kirimkan dokumen pendukung."

);


console.log(

    "\nADUAN EDGE TEST :",

    ADUAN_EDGE

);


// =====================================
// TEST UTAMA
// =====================================

async function runTest() {

    console.log("\n================================");

    console.log(
        "TEST MESSAGE HANDLER - EDGE CASES"
    );

    console.log("================================");


    // =================================
    // EDGE 1A
    // WARGA - JAWABAN INFO PERTAMA
    // =================================

    console.log(

        "\n=== EDGE 1A : WARGA - JAWABAN INFO PERTAMA ==="

    );


    stateService.clearState(

        WARGA

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                WARGA,

            notifyName:
                "Guz Memed",

            body:
                "Dokumen pendukung sudah saya siapkan.",

            hasQuotedMsg:
                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${ADUAN_EDGE}

Petugas meminta informasi berikut:

Mohon kirimkan dokumen pendukung.

Silakan balas pesan ini.`

        })

    );


    // =================================
    // EDGE 1B
    // WARGA - JAWABAN INFO GANDA
    // =================================

    console.log(

        "\n=== EDGE 1B : WARGA - JAWABAN INFO GANDA ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                WARGA,

            notifyName:
                "Guz Memed",

            body:
                "Saya kirim ulang dokumen.",

            hasQuotedMsg:
                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${ADUAN_EDGE}

Petugas meminta informasi berikut:

Mohon kirimkan dokumen pendukung.

Silakan balas pesan ini.`

        })

    );


    // =================================
    // EDGE 2
    // WARGA - JAWAB ADUAN SELESAI
    // =================================

    console.log(

        "\n=== EDGE 2 : WARGA - JAWAB ADUAN SELESAI ==="

    );


    stateService.clearState(

        WARGA

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                WARGA,

            notifyName:
                "Guz Memed",

            body:
                "Ini adalah jawaban tambahan.",

            hasQuotedMsg:
                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
ADU-20260718-0003

Petugas meminta informasi berikut:

Mohon kirimkan kembali dokumen pendukung terbaru.

Silakan balas pesan ini.`

        })

    );


    // =================================
    // EDGE 3
    // WARGA - NOMOR ADUAN TIDAK DITEMUKAN
    // =================================

    console.log(

        "\n=== EDGE 3 : WARGA - NOMOR ADUAN TIDAK DITEMUKAN ==="

    );


    stateService.clearState(

        WARGA

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                WARGA,

            notifyName:
                "Guz Memed",

            body:
                "Berikut informasi yang diminta.",

            hasQuotedMsg:
                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
ADU-20999999-9999

Petugas meminta informasi berikut:

Mohon kirimkan dokumen.

Silakan balas pesan ini.`

        })

    );


    // =================================
    // EDGE 4
    // PETUGAS - PILIHAN TIDAK VALID
    // =================================

    console.log(

        "\n=== EDGE 4 : PETUGAS - PILIHAN TIDAK VALID ==="

    );


    conversationService.clear(

        NAMA_PETUGAS

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                PETUGAS,

            notifyName:
                NAMA_PETUGAS,

            body:
                "9",

            hasQuotedMsg:
                true,

            quotedText:

`📢 *Jawaban Pelapor*

Nomor :
${ADUAN_EDGE}

Isi Aduan:

Aduan khusus pengujian edge case

Balas:

1. INFO ${ADUAN_EDGE}

2. SELESAIKAN ${ADUAN_EDGE}`

        })

    );


    // =================================
    // EDGE 5
    // PETUGAS - PESAN TANPA KONTEKS
    // =================================

    console.log(

        "\n=== EDGE 5 : PETUGAS - PESAN TANPA KONTEKS ==="

    );


    conversationService.clear(

        NAMA_PETUGAS

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                PETUGAS,

            notifyName:
                NAMA_PETUGAS,

            body:
                "Pesan tanpa konteks aduan."

        })

    );


    // =================================
    // SELESAI
    // =================================

    console.log("\n================================");

    console.log(

        "TEST EDGE CASES SELESAI"

    );

    console.log("================================");

}


// =====================================
// JALANKAN TEST
// =====================================

runTest()

    .catch(err => {

        console.error(

            "TEST EDGE ERROR:",

            err

        );

    });