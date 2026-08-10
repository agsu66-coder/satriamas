/**
 * ==========================================================
 * TEST INTEGRASI PROSES ADUAN TERATAI AI
 * ==========================================================
 *
 * Menguji proses production:
 *
 * Warga
 *   ↓
 * Aduan
 *   ↓
 * Owner
 *   ↓
 * INFO 1
 *   ↓
 * Jawaban Warga
 *   ↓
 * INFO 2
 *   ↓
 * Jawaban Warga
 *   ↓
 * INFO 3
 *   ↓
 * Jawaban Warga
 *   ↓
 * Owner menyelesaikan
 *   ↓
 * SELESAI
 *
 * Pengujian tambahan:
 *
 * - INFO ke-4 ditolak
 * - Petugas bukan Owner tidak dapat mengakses aduan aktif
 * - Aduan selesai tidak dapat diproses kembali
 *
 * ==========================================================
 */

const assert = require("assert");

const aduanService =
    require("../../bot/services/aduanService");

const petugasService =
    require("../../bot/services/petugasService");

const conversationService =
    require("../../bot/services/conversationService");

const petugasHandler =
    require("../../bot/handlers/petugasHandler");


// ==========================================================
// KONFIGURASI
// ==========================================================

const KATEGORI_ID = "KAT001";

const NOMOR_WARGA =
    "628999999999@c.us";


// ==========================================================
// DATA OWNER
// ==========================================================

const petugasAktif =
    petugasService.getByCategory(

        KATEGORI_ID

    );


console.log("=== DATA PETUGAS ===");

console.log(

    petugasAktif

);


console.log("====================");


if (

    !petugasAktif ||

    petugasAktif.length === 0

) {

    throw new Error(

        `Tidak ditemukan petugas aktif untuk kategori ${KATEGORI_ID}.`

    );

}


const owner =
    petugasAktif[0];


const namaOwner =
    owner.Nama_WA;


const nomorOwner =
    String(

        owner.Nomor_WA

    );


// ==========================================================
// MOCK CLIENT
// ==========================================================

const client = {

    sendMessage: async function(

        number,

        message

    ) {

        console.log("\n📤 MOCK SEND MESSAGE");

        console.log(

            "Tujuan :",

            number

        );

        console.log(

            "Pesan  :"

        );

        console.log(

            message

        );

        return {

            id: {

                _serialized:

                    "mock-message-id"

            }

        };

    }

};


// ==========================================================
// MOCK MESSAGE
// ==========================================================

function createMessage({

    from,

    body,

    namaWA,

    quotedText = "",

    hasQuotedMsg = false

}) {

    return {

        from,

        body,

        hasQuotedMsg,

        isStatus: false,

        fromMe: false,

        _data: {

            notifyName:

                namaWA,

            quotedMsg: {

                body:

                    quotedText

            }

        },

        reply: async function(

            message

        ) {

            console.log("\n📩 MOCK REPLY");

            console.log(

                message

            );

        }

    };

}


// ==========================================================
// UTILITAS
// ==========================================================

function lulus(

    keterangan

) {

    console.log(

        `✅ LULUS: ${keterangan}`

    );

}


function assertEqual(

    actual,

    expected,

    message

) {

    assert.strictEqual(

        actual,

        expected,

        message

    );

}


// ==========================================================
// PEMBUAT PESAN OWNER
// ==========================================================

function pesanOwner(

    body

) {

    return createMessage({

        from:

            nomorOwner,

        body,

        namaWA:

            namaOwner

    });

}


// ==========================================================
// PEMBUAT PESAN WARGA
// ==========================================================

function pesanWarga(

    body

) {

    return createMessage({

        from:

            NOMOR_WARGA,

        body,

        namaWA:

            "Warga Test"

    });

}


// ==========================================================
// MAIN TEST
// ==========================================================

(async function() {


    console.log("\n");

    console.log(

        "=========================================================="

    );

    console.log(

        "🧪 TEST INTEGRASI PROSES ADUAN TERATAI AI"

    );

    console.log(

        "=========================================================="

    );


    console.log("\n");

    console.log(

        "OWNER TEST:"

    );

    console.log(

        "ID       :",

        owner.ID

    );

    console.log(

        "Nama WA  :",

        owner.Nama_WA

    );

    console.log(

        "Nomor WA :",

        owner.Nomor_WA

    );


    // ======================================================
    // 1. MEMBUAT ADUAN
    // ======================================================

    const aduanId =

        aduanService.createComplaint({

            No_WA:

                NOMOR_WARGA,

            Nama:

                "Warga Test Integrasi",

            Kategori_ID:

                KATEGORI_ID,

            Isi:

                "Aduan untuk pengujian integrasi proses aduan."

        });


    const aduanAwal =

        aduanService.getById(

            aduanId

        );


    assert.ok(

        aduanAwal,

        "Aduan harus berhasil dibuat."

    );


    assertEqual(

        aduanAwal.Status,

        "BARU",

        "Status awal harus BARU."

    );


    assertEqual(

        aduanAwal.Owner,

        owner.ID,

        "Owner harus sesuai petugas kategori."

    );


    assertEqual(

        Number(

            aduanAwal.Jumlah_Info

        ),

        0,

        "Jumlah informasi awal harus 0."

    );


    lulus(

        "Aduan berhasil dibuat melalui aduanService production."

    );


    lulus(

        "Status awal aduan adalah BARU."

    );


    lulus(

        "Owner aduan sesuai dengan petugas kategori."

    );


    // ======================================================
    // 2. FUNGSI SIKLUS INFO
    // ======================================================

    async function prosesInfo(

        nomorSiklus,

        pertanyaan,

        jawaban

    ) {


        console.log("\n");

        console.log(

            `========== SIKLUS INFO ${nomorSiklus} ==========`

        );


        // --------------------------------------------------
        // OWNER MEMULAI INFO
        // --------------------------------------------------

        await petugasHandler.handlePetugas(

            client,

            pesanOwner(

                `INFO ${aduanId}`

            )

        );


        const sessionInfo =

            conversationService.get(

                namaOwner

            );


        assert.ok(

            sessionInfo,

            `Session INFO ke-${nomorSiklus} harus terbentuk.`

        );


        assertEqual(

            sessionInfo.mode,

            "INFO",

            `Mode harus INFO pada siklus ${nomorSiklus}.`

        );


        assertEqual(

            sessionInfo.aduanId,

            aduanId,

            "Session harus menunjuk aduan yang benar."

        );


        lulus(

            `Owner berhasil meminta informasi tambahan ke-${nomorSiklus}.`

        );


        // --------------------------------------------------
        // OWNER MENULIS PERTANYAAN
        // --------------------------------------------------

        await petugasHandler.handlePetugas(

            client,

            pesanOwner(

                pertanyaan

            )

        );


        const aduanSetelahInfo =

            aduanService.getById(

                aduanId

            );


        assertEqual(

            Number(

                aduanSetelahInfo.Jumlah_Info

            ),

            nomorSiklus,

            `Jumlah informasi harus ${nomorSiklus}.`

        );


        assertEqual(

            aduanSetelahInfo.Status,

            "MENUNGGU_INFO",

            "Status harus MENUNGGU_INFO."

        );


        lulus(

            `Permintaan informasi ke-${nomorSiklus} berhasil.`

        );


        lulus(

            `Jumlah informasi menjadi ${nomorSiklus}.`

        );


        lulus(

            `Status menjadi MENUNGGU_INFO setelah permintaan ke-${nomorSiklus}.`

        );


        // --------------------------------------------------
        // WARGA MENJAWAB
        // --------------------------------------------------

        aduanService.updateLastAnswer(

            aduanId,

            jawaban

        );


        const aduanSetelahJawaban =

            aduanService.getById(

                aduanId

            );


        assert.ok(

            aduanSetelahJawaban.Riwayat_Info.includes(

                jawaban

            ),

            "Jawaban warga harus masuk riwayat."

        );


        assertEqual(

            aduanSetelahJawaban.Status,

            "MENUNGGU_INFO",

            "Status tetap MENUNGGU_INFO."

        );


        lulus(

            `Jawaban warga ke-${nomorSiklus} berhasil.`

        );


        lulus(

            `Status tetap MENUNGGU_INFO setelah jawaban ke-${nomorSiklus}.`

        );


    }


    // ======================================================
    // 3. SIKLUS INFO 1
    // ======================================================

    await prosesInfo(

        1,

        "Mohon kirimkan informasi tambahan pertama.",

        "Berikut jawaban informasi tambahan pertama."

    );


    // ======================================================
    // 4. SIKLUS INFO 2
    // ======================================================

    await prosesInfo(

        2,

        "Mohon kirimkan informasi tambahan kedua.",

        "Berikut jawaban informasi tambahan kedua."

    );


    // ======================================================
    // 5. SIKLUS INFO 3
    // ======================================================

    await prosesInfo(

        3,

        "Mohon kirimkan informasi tambahan ketiga.",

        "Berikut jawaban informasi tambahan ketiga."

    );


    // ======================================================
    // 6. INFO KE-4 DITOLAK
    // ======================================================

    console.log("\n");

    console.log(

        "========== UJI BATAS INFORMASI =========="

    );


    await petugasHandler.handlePetugas(

        client,

        pesanOwner(

            `INFO ${aduanId}`

        )

    );


    const aduanSetelahInfoKe4 =

        aduanService.getById(

            aduanId

        );


    assertEqual(

        Number(

            aduanSetelahInfoKe4.Jumlah_Info

        ),

        3,

        "Jumlah informasi tidak boleh lebih dari 3."

    );


    lulus(

        "Permintaan informasi ke-4 ditolak."

    );


    lulus(

        "Jumlah informasi tetap maksimal 3."

    );


    // ======================================================
    // 7. UJI PETUGAS BUKAN OWNER
    // ======================================================

    console.log("\n");

    console.log(

        "========== UJI KEAMANAN OWNER =========="

    );


    const petugasBukanOwner =

        petugasService.getAll()

            .find(

                item =>

                    item.ID !== owner.ID &&

                    item.Aktif === "YA"

            );


    if (

        !petugasBukanOwner

    ) {

        throw new Error(

            "Tidak ditemukan petugas aktif lain."

        );

    }


    // ------------------------------------------------------
    // BUAT ADUAN AKTIF BARU
    // ------------------------------------------------------

    const aduanKeamananId =

        aduanService.createComplaint({

            No_WA:

                NOMOR_WARGA,

            Nama:

                "Warga Test Keamanan Owner",

            Kategori_ID:

                KATEGORI_ID,

            Isi:

                "Aduan untuk pengujian pembatasan Owner."

        });


    const aduanKeamanan =

        aduanService.getById(

            aduanKeamananId

        );


    assertEqual(

        aduanKeamanan.Status,

        "BARU",

        "Aduan keamanan harus BARU."

    );


    assertEqual(

        aduanKeamanan.Owner,

        owner.ID,

        "Aduan keamanan harus dimiliki Owner."

    );


    assertEqual(

        Number(

            aduanKeamanan.Jumlah_Info

        ),

        0,

        "Jumlah informasi awal harus 0."

    );


    lulus(

        "Aduan keamanan berhasil dibuat dalam kondisi aktif."

    );


    const pesanPetugasBukanOwner =

        createMessage({

            from:

                String(

                    petugasBukanOwner.Nomor_WA

                ),

            body:

                `INFO ${aduanKeamananId}`,

            namaWA:

                petugasBukanOwner.Nama_WA

        });


    const statusSebelum =

        aduanKeamanan.Status;


    const jumlahInfoSebelum =

        Number(

            aduanKeamanan.Jumlah_Info

        );


    await petugasHandler.handlePetugas(

        client,

        pesanPetugasBukanOwner

    );


    const aduanSetelahPercobaan =

        aduanService.getById(

            aduanKeamananId

        );


    // ------------------------------------------------------
    // VERIFIKASI
    // ------------------------------------------------------

    assertEqual(

        aduanSetelahPercobaan.Status,

        statusSebelum,

        "Status tidak boleh berubah."

    );


    assertEqual(

        Number(

            aduanSetelahPercobaan.Jumlah_Info

        ),

        jumlahInfoSebelum,

        "Jumlah_Info tidak boleh berubah."

    );


    lulus(

        "Petugas bukan Owner tidak mengubah status aduan."

    );


    lulus(

        "Petugas bukan Owner tidak menambah jumlah informasi."

    );


    // ======================================================
    // 8. OWNER MENYELESAIKAN ADUAN
    // ======================================================

    console.log("\n");

    console.log(

        "========== PENYELESAIAN ADUAN =========="

    );


    await petugasHandler.handlePetugas(

        client,

        pesanOwner(

            `SELESAIKAN ${aduanId}`

        )

    );


    const sessionFeedback =

        conversationService.get(

            namaOwner

        );


    assert.ok(

        sessionFeedback,

        "Session FEEDBACK harus terbentuk."

    );


    assertEqual(

        sessionFeedback.mode,

        "FEEDBACK",

        "Mode harus FEEDBACK."

    );


    assertEqual(

        sessionFeedback.aduanId,

        aduanId,

        "Feedback harus menunjuk aduan yang benar."

    );


    lulus(

        "Owner berhasil memulai proses penyelesaian aduan."

    );


    const feedback =

        "Aduan telah ditindaklanjuti sesuai kewenangan.";


    await petugasHandler.handlePetugas(

        client,

        pesanOwner(

            feedback

        )

    );


    const aduanSelesai =

        aduanService.getById(

            aduanId

        );


    assertEqual(

        aduanSelesai.Status,

        "SELESAI",

        "Status harus SELESAI."

    );


    assertEqual(

        aduanSelesai.Feedback,

        feedback,

        "Feedback harus tersimpan."

    );


    lulus(

        "Owner berhasil menyelesaikan aduan."

    );


    lulus(

        "Status berubah menjadi SELESAI."

    );


    // ======================================================
    // 9. ADUAN SELESAI TIDAK DAPAT DIPROSES LAGI
    // ======================================================

    console.log("\n");

    console.log(

        "========== UJI ADUAN SELESAI =========="

    );


    await petugasHandler.handlePetugas(

        client,

        pesanOwner(

            `INFO ${aduanId}`

        )

    );


    const aduanFinal =

        aduanService.getById(

            aduanId

        );


    assertEqual(

        aduanFinal.Status,

        "SELESAI",

        "Aduan selesai tidak boleh berubah status."

    );


    assertEqual(

        Number(

            aduanFinal.Jumlah_Info

        ),

        3,

        "Jumlah informasi tetap 3."

    );


    lulus(

        "Aduan selesai tidak dapat meminta informasi tambahan."

    );


    // ======================================================
    // HASIL AKHIR
    // ======================================================

    console.log("\n");

    console.log(

        "=========================================================="

    );

    console.log(

        "🎉 TEST INTEGRASI SELESAI"

    );

    console.log(

        "=========================================================="

    );


})()

.catch(

    err => {

        console.log("\n");

        console.log(

            "=========================================================="

        );

        console.log(

            "❌ TEST INTEGRASI GAGAL"

        );

        console.log(

            "=========================================================="

        );


        console.error(err);

        process.exit(1);

    }

);