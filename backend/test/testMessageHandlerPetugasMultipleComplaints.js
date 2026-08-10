const messageHandler =
    require("../../bot/handlers/messageHandler");

const conversationService =
    require("../../bot/services/conversationService");

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

const PETUGAS =
    "6282227026480@c.us";

const NAMA_PETUGAS =
    "Rose";

const WARGA =
    "6287736833184@c.us";


// =====================================
// FUNGSI UTAMA TEST
// =====================================

async function runTest() {

    console.log("\n================================");

    console.log(
        "TEST PETUGAS - MULTIPLE COMPLAINTS"
    );

    console.log("================================");


    // =====================================
    // BUAT ADUAN A
    // =====================================

    console.log(
        "\n=== SETUP : BUAT ADUAN A ==="
    );


    const aduanA =
        aduanService.create({

            No_WA:
                WARGA,

            Nama:
                "Guz Memed",

            Kategori_ID:
                "KAT001",

            Isi:
                "Pengujian aduan A",

            Owner:
                "PTG001"

        });


    console.log(
        "ADUAN A :",
        aduanA
    );


    // =====================================
    // BUAT ADUAN B
    // =====================================

    console.log(
        "\n=== SETUP : BUAT ADUAN B ==="
    );


    const aduanB =
        aduanService.create({

            No_WA:
                WARGA,

            Nama:
                "Guz Memed",

            Kategori_ID:
                "KAT001",

            Isi:
                "Pengujian aduan B",

            Owner:
                "PTG001"

        });


    console.log(
        "ADUAN B :",
        aduanB
    );


    // =====================================
    // TEST 1
    // PETUGAS MEMINTA INFO ADUAN A
    // =====================================

    console.log(
        "\n=== TEST 1 : INFO ADUAN A ==="
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
                `INFO ${aduanA}`

        })

    );


    // =====================================
    // TEST 2
    // PETUGAS MENULIS INFO ADUAN A
    // =====================================

    console.log(
        "\n=== TEST 2 : MENULIS INFO ADUAN A ==="
    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                PETUGAS,

            notifyName:
                NAMA_PETUGAS,

            body:
                "Mohon kirimkan dokumen untuk Aduan A."

        })

    );


    // =====================================
    // TEST 3
    // PETUGAS MEMINTA INFO ADUAN B
    // =====================================

    console.log(
        "\n=== TEST 3 : INFO ADUAN B ==="
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
                `INFO ${aduanB}`

        })

    );


    // =====================================
    // TEST 4
    // PETUGAS MENULIS INFO ADUAN B
    // =====================================

    console.log(
        "\n=== TEST 4 : MENULIS INFO ADUAN B ==="
    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                PETUGAS,

            notifyName:
                NAMA_PETUGAS,

            body:
                "Mohon kirimkan dokumen untuk Aduan B."

        })

    );


    // =====================================
    // VERIFIKASI RIWAYAT INFORMASI
    // =====================================

    console.log(
        "\n=== VERIFIKASI RIWAYAT INFORMASI ==="
    );


    const hasilA =
        aduanService.getById(

            aduanA

        );


    const hasilB =
        aduanService.getById(

            aduanB

        );


    let berhasil =
        true;


    // -------------------------------------
    // CEK INFO A
    // -------------------------------------

    if (

        !hasilA.Riwayat_Info ||

        !hasilA.Riwayat_Info.includes(

            "Mohon kirimkan dokumen untuk Aduan A."

        )

    ) {

        console.log(
            "❌ Informasi Aduan A tidak tersimpan."
        );

        berhasil =
            false;

    }

    else {

        console.log(
            "✅ Informasi Aduan A tersimpan."
        );

    }


    // -------------------------------------
    // CEK INFO B
    // -------------------------------------

    if (

        !hasilB.Riwayat_Info ||

        !hasilB.Riwayat_Info.includes(

            "Mohon kirimkan dokumen untuk Aduan B."

        )

    ) {

        console.log(
            "❌ Informasi Aduan B tidak tersimpan."
        );

        berhasil =
            false;

    }

    else {

        console.log(
            "✅ Informasi Aduan B tersimpan."
        );

    }


    // -------------------------------------
    // CEK KONTAMINASI A ← B
    // -------------------------------------

    if (

        hasilA.Riwayat_Info &&

        hasilA.Riwayat_Info.includes(

            "Mohon kirimkan dokumen untuk Aduan B."

        )

    ) {

        console.log(
            "❌ Informasi Aduan B masuk ke Aduan A."
        );

        berhasil =
            false;

    }

    else {

        console.log(
            "✅ Aduan A tidak tercampur dengan Aduan B."
        );

    }


    // -------------------------------------
    // CEK KONTAMINASI B ← A
    // -------------------------------------

    if (

        hasilB.Riwayat_Info &&

        hasilB.Riwayat_Info.includes(

            "Mohon kirimkan dokumen untuk Aduan A."

        )

    ) {

        console.log(
            "❌ Informasi Aduan A masuk ke Aduan B."
        );

        berhasil =
            false;

    }

    else {

        console.log(
            "✅ Aduan B tidak tercampur dengan Aduan A."
        );

    }


    // =====================================
    // TEST 5
    // PETUGAS MENYELESAIKAN ADUAN A
    // =====================================

    console.log(
        "\n=== TEST 5 : SELESAIKAN ADUAN A ==="
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
                `SELESAIKAN ${aduanA}`

        })

    );


    // =====================================
    // TEST 6
    // PETUGAS MENULIS FEEDBACK ADUAN A
    // =====================================

    console.log(
        "\n=== TEST 6 : FEEDBACK ADUAN A ==="
    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                PETUGAS,

            notifyName:
                NAMA_PETUGAS,

            body:
                "Aduan A telah ditindaklanjuti."

        })

    );


    // =====================================
    // VERIFIKASI AKHIR
    // =====================================

    console.log(
        "\n=== VERIFIKASI AKHIR ==="
    );


    const finalA =
        aduanService.getById(

            aduanA

        );


    const finalB =
        aduanService.getById(

            aduanB

        );


    // -------------------------------------
    // CEK STATUS ADUAN A
    // -------------------------------------

    if (

        finalA.Status === "SELESAI"

    ) {

        console.log(
            "✅ Aduan A berstatus SELESAI."
        );

    }

    else {

        console.log(
            "❌ Aduan A tidak menjadi SELESAI."
        );

        berhasil =
            false;

    }


    // -------------------------------------
    // CEK FEEDBACK ADUAN A
    // -------------------------------------

    if (

        finalA.Feedback ===

        "Aduan A telah ditindaklanjuti."

    ) {

        console.log(
            "✅ Feedback Aduan A tersimpan."
        );

    }

    else {

        console.log(
            "❌ Feedback Aduan A tidak sesuai."
        );

        berhasil =
            false;

    }


    // -------------------------------------
    // CEK ADUAN B
    // -------------------------------------

    if (

        finalB.Status !== "SELESAI"

    ) {

        console.log(
            "✅ Aduan B tidak ikut diselesaikan."
        );

    }

    else {

        console.log(
            "❌ Aduan B ikut berubah menjadi SELESAI."
        );

        berhasil =
            false;

    }


    // =====================================
    // TAMPILKAN DATA AKHIR
    // =====================================

    console.log(
        "\n=== DATA AKHIR ADUAN A ==="
    );


    console.log({

        ID:
            finalA.ID,

        Status:
            finalA.Status,

        Feedback:
            finalA.Feedback,

        Riwayat_Info:
            finalA.Riwayat_Info

    });


    console.log(
        "\n=== DATA AKHIR ADUAN B ==="
    );


    console.log({

        ID:
            finalB.ID,

        Status:
            finalB.Status,

        Feedback:
            finalB.Feedback,

        Riwayat_Info:
            finalB.Riwayat_Info

    });


    // =====================================
    // HASIL AKHIR
    // =====================================

    console.log(
        "\n================================"
    );


    if (

        berhasil

    ) {

        console.log(
            "✅ TEST PETUGAS MULTIPLE COMPLAINTS BERHASIL"
        );

    }

    else {

        console.log(
            "❌ TEST PETUGAS MULTIPLE COMPLAINTS GAGAL"
        );

    }


    console.log(
        "================================"
    );


    console.log(
        "\nTEST SELESAI."
    );

}


// =====================================
// JALANKAN TEST
// =====================================

runTest()

    .catch(err => {

        console.error(

            "TEST PETUGAS MULTIPLE COMPLAINTS ERROR:",

            err

        );

    });