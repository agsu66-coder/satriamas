const messageHandler =
    require("../../bot/handlers/messageHandler");

const conversationService =
    require("../../bot/services/conversationService");

const aduanService =
    require("../../bot/services/aduanService");

const petugasService =
    require("../../bot/services/petugasService");


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
// DATA PETUGAS
// =====================================

const PETUGAS_A =
    "6282227026480@c.us";

const NAMA_PETUGAS_A =
    "Rose";

const PETUGAS_A_ID =
    "PTG001";


// =====================================
// BUAT PETUGAS B
// =====================================
//
// Sesuaikan data ini dengan mekanisme
// petugasService yang digunakan TERATAI AI.
//
// Jika PTG002 sudah ada di workbook,
// bagian ini dapat langsung digunakan.
//

const PETUGAS_B_ID =
    "PTG002";

const PETUGAS_B_WA =
    "6282227026481@c.us";

const PETUGAS_B_NAMA =
    "Petugas B";


// =====================================
// BUAT ADUAN MILIK PETUGAS B
// =====================================

const ADUAN_OWNER_B =
    aduanService.create({

        No_WA:
            "6287736833184@c.us",

        Nama:
            "Warga Ownership Test",

        Kategori_ID:
            "KAT002",

        Isi:
            "Aduan untuk pengujian ownership.",

        Owner:
            PETUGAS_B_ID

    });


// =====================================
// STATUS ADUAN
// =====================================

aduanService.updateStatus(

    ADUAN_OWNER_B,

    "DIPROSES"

);


console.log(

    "\nADUAN MILIK PETUGAS B :",

    ADUAN_OWNER_B

);


// =====================================
// PESAN REPLY PETUGAS
// =====================================

const quotedAnswer =

`📢 *Jawaban Pelapor*

Nomor :
${ADUAN_OWNER_B}

Isi Aduan:

Aduan untuk pengujian ownership.

Balas:

1. INFO ${ADUAN_OWNER_B}

2. SELESAIKAN ${ADUAN_OWNER_B}`;


// =====================================
// TEST UTAMA
// =====================================

async function runTest() {

    console.log("\n================================");

    console.log(

        "TEST MESSAGE HANDLER - OWNERSHIP"

    );

    console.log("================================");


    // =================================
    // OWNERSHIP 1
    // PETUGAS BUKAN PEMILIK
    // MENCOBA INFO
    // =================================

    console.log(

        "\n=== OWNERSHIP 1 : PETUGAS BUKAN PEMILIK - INFO ==="

    );


    conversationService.clear(

        NAMA_PETUGAS_A

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                PETUGAS_A,

            notifyName:
                NAMA_PETUGAS_A,

            body:
                "1",

            hasQuotedMsg:
                true,

            quotedText:
                quotedAnswer

        })

    );


    // =================================
    // OWNERSHIP 2
    // PETUGAS BUKAN PEMILIK
    // MENCOBA SELESAIKAN
    // =================================

    console.log(

        "\n=== OWNERSHIP 2 : PETUGAS BUKAN PEMILIK - SELESAIKAN ==="

    );


    conversationService.clear(

        NAMA_PETUGAS_A

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:
                PETUGAS_A,

            notifyName:
                NAMA_PETUGAS_A,

            body:
                "2",

            hasQuotedMsg:
                true,

            quotedText:
                quotedAnswer

        })

    );


    // =================================
    // CEK STATUS AKHIR
    // =================================

    const aduanAkhir =

        aduanService.getById(

            ADUAN_OWNER_B

        );


    console.log(

        "\n===== STATUS AKHIR ADUAN ====="

    );

    console.log({

        ID:
            aduanAkhir.ID,

        Owner:
            aduanAkhir.Owner,

        Status:
            aduanAkhir.Status

    });


    console.log(

        "=============================="

    );


    console.log("\n================================");

    console.log(

        "TEST OWNERSHIP SELESAI"

    );

    console.log("================================");

}


// =====================================
// JALANKAN TEST
// =====================================

runTest()

    .catch(err => {

        console.error(

            "TEST OWNERSHIP ERROR:",

            err

        );

    });