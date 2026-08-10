const aduanService =
    require("../../bot/services/aduanService");

const petugasService =
    require("../../bot/services/petugasService");

const conversationService =
    require("../../bot/services/conversationService");

const petugasHandler =
    require("../../bot/handlers/petugasHandler");


// =====================================
// DATA PETUGAS
// =====================================

const petugas =
    petugasService.getByName("Rose");


// =====================================
// MOCK CLIENT
// =====================================

const mockClient = {

    async sendMessage(to, text) {

        console.log("\n===== PESAN KE WARGA =====");

        console.log("KEPADA :", to);

        console.log("PESAN :");

        console.log(text);

        console.log("==========================\n");

    }

};


// =====================================
// MOCK MESSAGE
// =====================================

function createMsg(body) {

    return {

        body,

        from:
            "6282227026480@c.us",

        _data: {

            notifyName:
                "Rose"

        },

        hasQuotedMsg:
            false,

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
// TEST UTAMA
// =====================================

async function runTest() {

    console.log("================================");

    console.log("TEST LIFECYCLE ADUAN");

    console.log("PETUGAS :", petugas.Nama_WA);

    console.log("================================");


    // =================================
    // 1. BUAT ADUAN BARU
    // =================================

    console.log("\n=== TEST 1 : BUAT ADUAN BARU ===");

    const aduanId =
        aduanService.createComplaint({

            No_WA:
                "6287736833184@c.us",

            Nama:
                "Warga Test",

            Kategori_ID:
                "KAT001",

            Isi:
                "Test siklus lengkap aduan TERATAI AI"

        });


    let aduan =
        aduanService.getById(aduanId);


    console.log("ID      :", aduan.ID);

    console.log("STATUS  :", aduan.Status);

    console.log("OWNER   :", aduan.Owner);


    // =================================
    // 2. PROSES ADUAN
    // =================================

    console.log("\n=== TEST 2 : PETUGAS MEMPROSES ADUAN ===");


    conversationService.set(

        petugas.Nama_WA,

        {

            mode:
                "ADUAN_DETAIL",

            aduanId

        }

    );


    await petugasHandler.handlePetugas(

        mockClient,

        createMsg("1")

    );


    aduan =
        aduanService.getById(aduanId);


    console.log("STATUS :", aduan.Status);


    // =================================
    // 3. MINTA INFORMASI
    // =================================

    console.log("\n=== TEST 3 : PETUGAS MEMINTA INFORMASI ===");


    conversationService.set(

        petugas.Nama_WA,

        {

            mode:
                "INFO",

            aduanId

        }

    );


    await petugasHandler.handlePetugas(

        mockClient,

        createMsg(

            "Mohon lampirkan dokumen pendukung."

        )

    );


    aduan =
        aduanService.getById(aduanId);


    console.log("STATUS      :", aduan.Status);

    console.log(

        "JUMLAH INFO :",

        aduan.Jumlah_Info

    );


    // =================================
    // 4. SIMULASI JAWABAN WARGA
    // =================================

    console.log("\n=== TEST 4 : WARGA MEMBERIKAN INFORMASI ===");


    aduanService.updateLastAnswer(

        aduanId,

        "Dokumen pendukung sudah disiapkan."

    );


    aduanService.updateStatus(

        aduanId,

        "DIPROSES"

    );


    aduan =
        aduanService.getById(aduanId);


    console.log("STATUS :", aduan.Status);


    // =================================
    // 5. SELESAIKAN ADUAN
    // =================================

    console.log("\n=== TEST 5 : PETUGAS MENYELESAIKAN ADUAN ===");


    conversationService.set(

        petugas.Nama_WA,

        {

            mode:
                "FEEDBACK",

            aduanId

        }

    );


    await petugasHandler.handlePetugas(

        mockClient,

        createMsg(

            "Permohonan telah ditindaklanjuti oleh petugas."

        )

    );


    aduan =
        aduanService.getById(aduanId);


    console.log("STATUS   :", aduan.Status);

    console.log("FEEDBACK :", aduan.Feedback);


    // =================================
    // 6. HASIL AKHIR
    // =================================

    console.log("\n================================");

    console.log("RINGKASAN LIFECYCLE");

    console.log("================================");

    console.log({

        ID:
            aduan.ID,

        Status:
            aduan.Status,

        Jumlah_Info:
            aduan.Jumlah_Info,

        Feedback:
            aduan.Feedback,

        Riwayat_Info:
            aduan.Riwayat_Info

    });


    console.log("\n================================");

    console.log("TEST SELESAI");

    console.log("================================");

}


runTest();