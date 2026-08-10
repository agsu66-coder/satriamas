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

        async getContact() {

            return {

                id: {

                    _serialized: from

                }

            };

        },

        async reply(text) {

            console.log("\n===== BALASAN BOT =====");

            console.log(text);

            console.log("=======================\n");

        }

    };

}


// =====================================
// DATA PENGUJIAN
// =====================================

const WARGA =
    "6287736833184@c.us";

const PETUGAS =
    "6282227026480@c.us";

const NAMA_WARGA =
    "Guz Memed";

const NAMA_PETUGAS =
    "Rose";


// =====================================
// MAIN TEST
// =====================================

async function runTest() {

    console.log("\n================================");

    console.log(
        "TEST COMPLAINT END-TO-END"
    );

    console.log("================================");


    // =================================
    // RESET STATE
    // =================================

    stateService.clearState(

        WARGA

    );

    conversationService.clear(

        NAMA_PETUGAS

    );


    // =================================
    // STEP 1
    // WARGA MEMULAI PENGADUAN
    // =================================

    console.log(

        "\n=== STEP 1 : WARGA MEMULAI PENGADUAN ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                WARGA,

            notifyName:

                NAMA_WARGA,

            body:

                "PENGADUAN"

        })

    );


    // =================================
    // STEP 2
    // WARGA MEMILIH KATEGORI
    // =================================

    console.log(

        "\n=== STEP 2 : WARGA MEMILIH KATEGORI ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                WARGA,

            notifyName:

                NAMA_WARGA,

            body:

                "1"

        })

    );


    // =================================
    // STEP 3
    // WARGA MENULIS ADUAN
    // =================================

    console.log(

        "\n=== STEP 3 : WARGA MENULIS ADUAN ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                WARGA,

            notifyName:

                NAMA_WARGA,

            body:

                "Saya ingin melaporkan permasalahan pelayanan."

        })

    );


    // =================================
    // CARI ADUAN TERBARU
    // =================================

    const complaints =
        aduanService.getAll
            ? aduanService.getAll()
            : [];


    const aduan =
        complaints

            .filter(

                item =>

                    item.No_WA === WARGA

            )

            .sort(

                (a, b) =>

                    b.ID.localeCompare(a.ID)

            )[0];


    if (!aduan) {

        throw new Error(

            "Aduan tidak ditemukan setelah warga membuat aduan."

        );

    }


    const ADUAN_ID =
        aduan.ID;


    console.log(

        "ADUAN TERBENTUK :",

        ADUAN_ID

    );


    // =================================
    // STEP 4
    // PETUGAS MEMINTA INFORMASI
    // =================================

    console.log(

        "\n=== STEP 4 : PETUGAS MEMINTA INFORMASI ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                PETUGAS,

            notifyName:

                NAMA_PETUGAS,

            body:

                `INFO ${ADUAN_ID}`

        })

    );


    // =================================
    // STEP 5
    // PETUGAS MENULIS INFORMASI
    // =================================

    console.log(

        "\n=== STEP 5 : PETUGAS MENULIS INFORMASI ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                PETUGAS,

            notifyName:

                NAMA_PETUGAS,

            body:

                "Mohon kirimkan dokumen pendukung."

        })

    );


    // =================================
    // STEP 6
    // WARGA MENJAWAB INFORMASI
    // =================================

    console.log(

        "\n=== STEP 6 : WARGA MENJAWAB INFORMASI ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                WARGA,

            notifyName:

                NAMA_WARGA,

            body:

                "Dokumen pendukung sudah saya siapkan.",

            hasQuotedMsg:

                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${ADUAN_ID}

Petugas meminta informasi berikut:

Mohon kirimkan dokumen pendukung.

Silakan balas pesan ini.`

        })

    );


    // =================================
    // STEP 7
    // PETUGAS MEMINTA INFORMASI KEDUA
    // =================================

    console.log(

        "\n=== STEP 7 : PETUGAS MEMINTA INFORMASI KEDUA ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                PETUGAS,

            notifyName:

                NAMA_PETUGAS,

            body:

                `INFO ${ADUAN_ID}`

        })

    );


    // =================================
    // STEP 8
    // PETUGAS MENULIS INFORMASI KEDUA
    // =================================

    console.log(

        "\n=== STEP 8 : PETUGAS MENULIS INFORMASI KEDUA ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                PETUGAS,

            notifyName:

                NAMA_PETUGAS,

            body:

                "Mohon konfirmasi waktu kejadian."

        })

    );


    // =================================
    // STEP 9
    // WARGA MENJAWAB INFORMASI KEDUA
    // =================================

    console.log(

        "\n=== STEP 9 : WARGA MENJAWAB INFORMASI KEDUA ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                WARGA,

            notifyName:

                NAMA_WARGA,

            body:

                "Kejadian berlangsung pada hari Senin.",

            hasQuotedMsg:

                true,

            quotedText:

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${ADUAN_ID}

Petugas meminta informasi berikut:

Mohon konfirmasi waktu kejadian.

Silakan balas pesan ini.`

        })

    );


    // =================================
    // STEP 10
    // PETUGAS MENYELESAIKAN ADUAN
    // =================================

    console.log(

        "\n=== STEP 10 : PETUGAS MENYELESAIKAN ADUAN ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                PETUGAS,

            notifyName:

                NAMA_PETUGAS,

            body:

                `SELESAIKAN ${ADUAN_ID}`

        })

    );


    // =================================
    // STEP 11
    // PETUGAS MENULIS FEEDBACK
    // =================================

    console.log(

        "\n=== STEP 11 : PETUGAS MENULIS FEEDBACK ==="

    );


    await messageHandler.handleMessage(

        mockClient,

        createMsg({

            from:

                PETUGAS,

            notifyName:

                NAMA_PETUGAS,

            body:

                "Aduan telah ditindaklanjuti dan diteruskan kepada bagian terkait."

        })

    );


    // =================================
    // VERIFIKASI AKHIR
    // =================================

    console.log(

        "\n================================"

    );

    console.log(

        "VERIFIKASI AKHIR"

    );

    console.log(

        "================================"

    );


    const hasil =
        aduanService.getById(

            ADUAN_ID

        );


    if (!hasil) {

        throw new Error(

            "Aduan tidak ditemukan pada verifikasi akhir."

        );

    }


    console.log({

        ID:

            hasil.ID,

        Status:

            hasil.Status,

        Feedback:

            hasil.Feedback,

        Jumlah_Info:

            hasil.Jumlah_Info,

        Riwayat_Info:

            hasil.Riwayat_Info

    });


    if (

        hasil.Status !== "SELESAI"

    ) {

        throw new Error(

            "Status akhir aduan bukan SELESAI."

        );

    }


    if (

        !hasil.Feedback

    ) {

        throw new Error(

            "Feedback aduan kosong."

        );

    }


    if (

        hasil.Jumlah_Info < 2

    ) {

        throw new Error(

            "Jumlah informasi seharusnya minimal 2."

        );

    }


    if (

        !hasil.Riwayat_Info.includes(

            "Mohon kirimkan dokumen pendukung."

        )

    ) {

        throw new Error(

            "Informasi pertama tidak ditemukan."

        );

    }


    if (

        !hasil.Riwayat_Info.includes(

            "Mohon konfirmasi waktu kejadian."

        )

    ) {

        throw new Error(

            "Informasi kedua tidak ditemukan."

        );

    }


    if (

        !hasil.Riwayat_Info.includes(

            "Dokumen pendukung sudah saya siapkan."

        )

    ) {

        throw new Error(

            "Jawaban pertama warga tidak ditemukan."

        );

    }


    if (

        !hasil.Riwayat_Info.includes(

            "Kejadian berlangsung pada hari Senin."

        )

    ) {

        throw new Error(

            "Jawaban kedua warga tidak ditemukan."

        );

    }


    console.log(

        "\n✅ Aduan berhasil dibuat."

    );


    console.log(

        "✅ Informasi tambahan pertama berhasil dikirim."

    );


    console.log(

        "✅ Jawaban warga pertama berhasil disimpan."

    );


    console.log(

        "✅ Informasi tambahan kedua berhasil dikirim."

    );


    console.log(

        "✅ Jawaban warga kedua berhasil disimpan."

    );


    console.log(

        "✅ Aduan berhasil diselesaikan."

    );


    console.log(

        "✅ Feedback berhasil disimpan."

    );


    console.log(

        "\n================================"

    );


    console.log(

        "✅ TEST COMPLAINT END-TO-END BERHASIL"

    );


    console.log(

        "================================"

    );

}


// =====================================
// JALANKAN TEST
// =====================================

runTest()

    .catch(

        err => {

            console.error(

                "\n❌ TEST COMPLAINT END-TO-END GAGAL"

            );

            console.error(

                err

            );

        }

    );