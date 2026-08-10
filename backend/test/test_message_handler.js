const messageHandler =
    require("../../bot/handlers/messageHandler");

const conversationService =
    require("../../bot/services/conversationService");

const stateService =
    require("../../bot/services/stateService");


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

            notifyName: notifyName,

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
// ADUAN UNTUK TEST 5-8
// =====================================

const ADUAN_PROSES =
    "ADU-20260717-0005";


// =====================================
// ADUAN UNTUK TEST 9
// STATUS HARUS MENUNGGU_INFO
// =====================================

const ADUAN_TEST_INFO =
    "ADU-20260718-0003";


// =====================================
// TEST UTAMA
// =====================================

async function runTest() {

    console.log("\n================================");

    console.log("TEST MESSAGE HANDLER ROUTER");

    console.log("================================");


    // =================================
    // TEST 1
    // WARGA - MENU UTAMA
    // =================================

    console.log(
        "\n=== TEST 1 : WARGA - MENU UTAMA ==="
    );

    stateService.clearState(WARGA);

    conversationService.clear(

        NAMA_PETUGAS

    );

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: WARGA,

            notifyName: "Warga Test",

            body: "Halo"

        })

    );


    // =================================
    // TEST 2
    // WARGA - ADMINISTRASI
    // =================================

    console.log(
        "\n=== TEST 2 : WARGA - ADMINISTRASI ==="
    );

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: WARGA,

            notifyName: "Warga Test",

            body: "1"

        })

    );


    // =================================
    // TEST 3
    // WARGA - PENGADUAN
    // =================================

    console.log(
        "\n=== TEST 3 : WARGA - PENGADUAN ==="
    );

    stateService.clearState(WARGA);

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: WARGA,

            notifyName: "Warga Test",

            body: "2"

        })

    );


    // =================================
    // TEST 4
    // PETUGAS - DASHBOARD
    // =================================

    console.log(
        "\n=== TEST 4 : PETUGAS - DASHBOARD ==="
    );

    conversationService.set(

        NAMA_PETUGAS,

        {

            mode: "DASHBOARD"

        }

    );

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: PETUGAS,

            notifyName: NAMA_PETUGAS,

            body: "1"

        })

    );


    // =================================
    // TEST 5
    // PETUGAS - DETAIL ADUAN
    // =================================

    console.log(
        "\n=== TEST 5 : PETUGAS - DETAIL ADUAN ==="
    );

    conversationService.set(

        NAMA_PETUGAS,

        {

            mode: "ADUAN_DETAIL",

            ownerId: "PTG001",

            aduanId: ADUAN_PROSES

        }

    );

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: PETUGAS,

            notifyName: NAMA_PETUGAS,

            body: "1"

        })

    );


    // =================================
    // TEST 6
    // PETUGAS - PILIH TINDAKAN
    // =================================

    console.log(
        "\n=== TEST 6 : PETUGAS - PILIH TINDAKAN ==="
    );

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: PETUGAS,

            notifyName: NAMA_PETUGAS,

            body: "1"

        })

    );


    // =================================
    // TEST 7
    // PETUGAS - INFO
    // =================================

    console.log(
        "\n=== TEST 7 : PETUGAS - INFO ==="
    );

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: PETUGAS,

            notifyName: NAMA_PETUGAS,

            body:
                "Mohon lampirkan dokumen."

        })

    );


    // =================================
    // TEST 8
    // PETUGAS - FEEDBACK
    // =================================

    console.log(
        "\n=== TEST 8 : PETUGAS - FEEDBACK ==="
    );

    conversationService.set(

        NAMA_PETUGAS,

        {

            mode: "FEEDBACK",

            aduanId: ADUAN_PROSES

        }

    );

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: PETUGAS,

            notifyName: NAMA_PETUGAS,

            body:
                "Aduan telah ditindaklanjuti."

        })

    );


    // =================================
    // TEST 9
    // WARGA - BALAS INFORMASI TAMBAHAN
    // =================================

    console.log(
        "\n=== TEST 9 : WARGA - BALAS INFORMASI TAMBAHAN ==="
    );

    stateService.clearState(WARGA);

    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from: WARGA,

            notifyName: "Guz Memed",

            body:

                "Berikut dokumen yang diminta.",

            hasQuotedMsg: true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${ADUAN_TEST_INFO}

Petugas meminta informasi berikut:

Mohon lampirkan dokumen.

Silakan balas pesan ini.`

        })

    );


// =====================================
// TEST 10
// PETUGAS - MINTA INFORMASI LAGI
// =====================================

console.log(
    "\n=== TEST 10 : PETUGAS - MINTA INFORMASI LAGI ==="
);


// Pastikan session petugas bersih

conversationService.clear(

    NAMA_PETUGAS

);


// Petugas melakukan REPLY
// terhadap pesan jawaban warga
// yang berisi Nomor Aduan

await messageHandler.handleMessage(

    mockClient,

    createMsg({

        from: PETUGAS,

        notifyName: NAMA_PETUGAS,

        body: "1",

        hasQuotedMsg: true,

        quotedText:

`📢 *Jawaban Pelapor*

Nomor :
ADU-20260718-0003

Isi Aduan:

Mih kangen

Riwayat:

[INFO-1]
Petugas :
kangen kamu juga

Jawaban Warga :
Berikut dokumen yang diminta.

Balas:

1. INFO ADU-20260718-0003

2. SELESAIKAN ADU-20260718-0003`

    })

);

// =====================================
// TEST 11
// PETUGAS - MENULIS PERTANYAAN INFO
// =====================================

console.log(
    "\n=== TEST 11 : PETUGAS - MENULIS PERTANYAAN INFO ==="
);

await messageHandler.handleMessage(

    mockClient,

    createMsg({

        from: PETUGAS,

        notifyName: NAMA_PETUGAS,

        body:
            "Mohon kirimkan kembali dokumen pendukung terbaru."

    })

);

// =====================================
// TEST 12
// WARGA - MEMBALAS INFORMASI TAMBAHAN KEDUA
// =====================================

console.log(
    "\n=== TEST 12 : WARGA - BALAS INFORMASI KEDUA ==="
);

await messageHandler.handleMessage(

    mockClient,

    createMsg({

        from: WARGA,

        notifyName: "Guz Memed",

        body:
            "Dokumen terbaru sudah saya kirimkan kembali.",

        hasQuotedMsg: true,

        quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${ADUAN_TEST_INFO}

Petugas meminta informasi berikut:

Mohon kirimkan kembali dokumen pendukung terbaru.

Silakan balas pesan ini.`

    })

);

// =====================================
// TEST 13
// PETUGAS - MENYELESAIKAN ADUAN
// =====================================

console.log(
    "\n=== TEST 13 : PETUGAS - MENYELESAIKAN ADUAN ==="
);

await messageHandler.handleMessage(

    mockClient,

    createMsg({

        from: PETUGAS,

        notifyName: NAMA_PETUGAS,

        body: "2",

        hasQuotedMsg: true,

        quotedText:

`📢 *Jawaban Pelapor*

Nomor :
ADU-20260718-0003

Isi Aduan:

Mih kangen

Riwayat:

[INFO-1]
Petugas :
kangen kamu juga

Jawaban Warga :
Berikut dokumen yang diminta.

[INFO-2]
Petugas :
Mohon kirimkan kembali dokumen pendukung terbaru.

Jawaban Warga :
Berikut dokumen yang diminta.

[INFO-3]
Petugas :
Mohon kirimkan kembali dokumen pendukung terbaru.

Jawaban Warga :
Dokumen terbaru sudah saya kirimkan kembali.

Balas:

1. INFO ADU-20260718-0003

2. SELESAIKAN ADU-20260718-0003`

    })

);

// =====================================
// TEST 14
// PETUGAS - MENULIS FEEDBACK
// =====================================

console.log(
    "\n=== TEST 14 : PETUGAS - MENULIS FEEDBACK ==="
);

await messageHandler.handleMessage(

    mockClient,

    createMsg({

        from: PETUGAS,

        notifyName: NAMA_PETUGAS,

        body:
            "Aduan telah ditindaklanjuti dan selesai."

    })

);

// =====================================
// SELESAI
// =====================================

console.log("\n================================");

console.log("TEST MESSAGE HANDLER SELESAI");

console.log("================================");

}


// =====================================
// JALANKAN TEST
// =====================================

runTest()

    .catch(err => {

        console.error(

            "TEST ERROR:",

            err

        );

    });