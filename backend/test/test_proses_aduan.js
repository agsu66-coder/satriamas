/**
 * ==========================================================
 * TEST BASELINE PROSES ADUAN TERATAI AI
 * ==========================================================
 *
 * Tujuan:
 * Menguji proses dasar aduan, termasuk:
 *
 * 1. Aduan baru
 * 2. Validasi Owner
 * 3. Permintaan informasi tambahan
 * 4. Jawaban warga
 * 5. Maksimal 3 siklus informasi tambahan
 * 6. Penolakan permintaan informasi ke-4
 * 7. Penyelesaian aduan
 * 8. Pencegahan akses petugas lain
 * 9. Dashboard ringkasan
 *
 * File ini tidak mengubah:
 * - TERATAI_CORE.xlsx
 * - Kode production
 *
 * Jalankan:
 *
 * node test_proses_aduan.js
 *
 */


// ==========================================================
// DATA SIMULASI ADUAN UTAMA
// ==========================================================

const aduan = {

    ID: "ADU-20260721-0001",

    No_WA: "628123456789",

    Nama: "Warga",

    Kategori_ID: "KAT-001",

    Isi: "Contoh aduan",

    Status: "BARU",

    Owner: "PTG-001",

    Feedback: "",

    Jumlah_Info: 0,

    Riwayat_Info: "",

    Tanggal_Update:
        "2026-07-21 10:00:00"

};


// ==========================================================
// DATA SIMULASI PETUGAS
// ==========================================================

const petugasOwner = {

    ID: "PTG-001",

    Nama: "Petugas Owner"

};


const petugasLain = {

    ID: "PTG-002",

    Nama: "Petugas Lain"

};


// ==========================================================
// ASSERT
// ==========================================================

function assert(

    condition,

    message

) {

    if (!condition) {

        throw new Error(

            "❌ GAGAL: " + message

        );

    }

    console.log(

        "✅ LULUS: " + message

    );

}


// ==========================================================
// VALIDASI OWNER
// ==========================================================

function isOwner(

    petugas,

    aduan

) {

    return (

        petugas.ID ===

        aduan.Owner

    );

}


// ==========================================================
// PERMINTAAN INFORMASI TAMBAHAN
// ==========================================================

function requestInformation(

    petugas,

    aduan,

    pertanyaan

) {


    // =====================================
    // VALIDASI OWNER
    // =====================================

    if (

        !isOwner(

            petugas,

            aduan

        )

    ) {

        return {

            success: false,

            message:

                "Petugas bukan Owner aduan."

        };

    }


    // =====================================
    // ADUAN SELESAI
    // =====================================

    if (

        aduan.Status ===

        "SELESAI"

    ) {

        return {

            success: false,

            message:

                "Aduan sudah selesai."

        };

    }


    // =====================================
    // BATAS MAKSIMAL 3 INFORMASI
    // =====================================

    if (

        aduan.Jumlah_Info >= 3

    ) {

        return {

            success: false,

            message:

                "Batas informasi telah tercapai."

        };

    }


    // =====================================
    // TAMBAH JUMLAH INFORMASI
    // =====================================

    aduan.Jumlah_Info++;


    // =====================================
    // SIMPAN RIWAYAT
    // =====================================

    aduan.Riwayat_Info +=

`

[INFO-${aduan.Jumlah_Info}]

Petugas:

${pertanyaan}

`.trim();


    // =====================================
    // UPDATE STATUS
    // =====================================

    aduan.Status =

        "MENUNGGU_INFO";


    return {

        success: true

    };

}


// ==========================================================
// JAWABAN WARGA
// ==========================================================

function citizenAnswer(

    aduan,

    nomorWA,

    jawaban

) {


    // =====================================
    // VALIDASI PEMILIK ADUAN
    // =====================================

    if (

        aduan.No_WA !==

        nomorWA

    ) {

        return {

            success: false,

            message:

                "Bukan pemilik aduan."

        };

    }


    // =====================================
    // ADUAN SELESAI
    // =====================================

    if (

        aduan.Status ===

        "SELESAI"

    ) {

        return {

            success: false,

            message:

                "Aduan sudah selesai."

        };

    }


    // =====================================
    // SIMPAN JAWABAN
    // =====================================

    aduan.Riwayat_Info +=

`

Jawaban Warga:

${jawaban}

`.trim();


    return {

        success: true

    };

}


// ==========================================================
// PENYELESAIAN ADUAN
// ==========================================================

function finishComplaint(

    petugas,

    aduan,

    feedback

) {


    // =====================================
    // VALIDASI OWNER
    // =====================================

    if (

        !isOwner(

            petugas,

            aduan

        )

    ) {

        return {

            success: false,

            message:

                "Petugas bukan Owner aduan."

        };

    }


    // =====================================
    // ADUAN SUDAH SELESAI
    // =====================================

    if (

        aduan.Status ===

        "SELESAI"

    ) {

        return {

            success: false,

            message:

                "Aduan sudah selesai."

        };

    }


    // =====================================
    // SIMPAN FEEDBACK
    // =====================================

    aduan.Feedback =

        feedback;


    // =====================================
    // UPDATE STATUS
    // =====================================

    aduan.Status =

        "SELESAI";


    return {

        success: true

    };

}


// ==========================================================
// DASHBOARD RINGKASAN
// ==========================================================

function dashboardSummary(

    petugas,

    daftarAduan

) {


    const milikPetugas =

        daftarAduan.filter(

            item =>

                item.Owner ===

                petugas.ID

        );


    return {

        total:

            milikPetugas.length,


        baru:

            milikPetugas.filter(

                item =>

                    item.Status ===

                    "BARU"

            ).length,


        diproses:

            milikPetugas.filter(

                item =>

                    item.Status ===

                    "DIPROSES"

            ).length,


        menungguInfo:

            milikPetugas.filter(

                item =>

                    item.Status ===

                    "MENUNGGU_INFO"

            ).length,


        selesai:

            milikPetugas.filter(

                item =>

                    item.Status ===

                    "SELESAI"

            ).length

    };

}


// ==========================================================
// MULAI TEST
// ==========================================================

console.log(`

==========================================================

🧪 TEST BASELINE PROSES ADUAN TERATAI AI

==========================================================

`);


// ==========================================================
// TEST 1
// ==========================================================

assert(

    aduan.Status ===

    "BARU",

    "Aduan baru memiliki status BARU."

);


// ==========================================================
// TEST 2
// ==========================================================

assert(

    aduan.Owner ===

    petugasOwner.ID,

    "Aduan memiliki Owner yang valid."

);


// ==========================================================
// TEST SIKLUS INFORMASI KE-1
// ==========================================================

const info1 =

    requestInformation(

        petugasOwner,

        aduan,

        "Mohon informasi tambahan pertama."

    );


assert(

    info1.success === true,

    "Permintaan informasi ke-1 berhasil."

);


assert(

    aduan.Jumlah_Info === 1,

    "Jumlah informasi menjadi 1."

);


assert(

    aduan.Status ===

    "MENUNGGU_INFO",

    "Status menjadi MENUNGGU_INFO setelah permintaan ke-1."

);


const answer1 =

    citizenAnswer(

        aduan,

        "628123456789",

        "Jawaban informasi pertama."

    );


assert(

    answer1.success === true,

    "Jawaban warga ke-1 berhasil."

);


// ==========================================================
// TEST SIKLUS INFORMASI KE-2
// ==========================================================

const info2 =

    requestInformation(

        petugasOwner,

        aduan,

        "Mohon informasi tambahan kedua."

    );


assert(

    info2.success === true,

    "Permintaan informasi ke-2 berhasil."

);


assert(

    aduan.Jumlah_Info === 2,

    "Jumlah informasi menjadi 2."

);


const answer2 =

    citizenAnswer(

        aduan,

        "628123456789",

        "Jawaban informasi kedua."

    );


assert(

    answer2.success === true,

    "Jawaban warga ke-2 berhasil."

);


// ==========================================================
// TEST SIKLUS INFORMASI KE-3
// ==========================================================

const info3 =

    requestInformation(

        petugasOwner,

        aduan,

        "Mohon informasi tambahan ketiga."

    );


assert(

    info3.success === true,

    "Permintaan informasi ke-3 berhasil."

);


assert(

    aduan.Jumlah_Info === 3,

    "Jumlah informasi menjadi 3."

);


const answer3 =

    citizenAnswer(

        aduan,

        "628123456789",

        "Jawaban informasi ketiga."

    );


assert(

    answer3.success === true,

    "Jawaban warga ke-3 berhasil."

);


// ==========================================================
// TEST PERMINTAAN INFORMASI KE-4
// ==========================================================

const info4 =

    requestInformation(

        petugasOwner,

        aduan,

        "Mohon informasi tambahan keempat."

    );


assert(

    info4.success === false,

    "Permintaan informasi ke-4 ditolak."

);


assert(

    aduan.Jumlah_Info === 3,

    "Jumlah informasi tidak melebihi batas 3."

);


// ==========================================================
// TEST PETUGAS LAIN
// ==========================================================

const wrongInfoResult =

    requestInformation(

        petugasLain,

        aduan,

        "Permintaan dari petugas lain."

    );


assert(

    wrongInfoResult.success === false,

    "Petugas bukan Owner tidak dapat meminta informasi."

);


// ==========================================================
// TEST PEMILIK ADUAN
// ==========================================================

const wrongAnswerResult =

    citizenAnswer(

        aduan,

        "628999999999",

        "Jawaban dari nomor lain."

    );


assert(

    wrongAnswerResult.success === false,

    "Nomor lain tidak dapat memberikan jawaban."

);


// ==========================================================
// TEST PENYELESAIAN
// ==========================================================

const finishResult =

    finishComplaint(

        petugasOwner,

        aduan,

        "Aduan telah ditindaklanjuti."

    );


assert(

    finishResult.success === true,

    "Owner dapat menyelesaikan aduan."

);


assert(

    aduan.Status ===

    "SELESAI",

    "Status berubah menjadi SELESAI."

);


// ==========================================================
// TEST PETUGAS LAIN TIDAK DAPAT MENYELESAIKAN
// ==========================================================

const wrongFinishResult =

    finishComplaint(

        petugasLain,

        aduan,

        "Penyelesaian dari petugas lain."

    );


assert(

    wrongFinishResult.success === false,

    "Petugas bukan Owner tidak dapat menyelesaikan aduan."

);


// ==========================================================
// TEST ADUAN SELESAI
// ==========================================================

const afterFinishInfo =

    requestInformation(

        petugasOwner,

        aduan,

        "Informasi setelah selesai."

    );


assert(

    afterFinishInfo.success === false,

    "Aduan selesai tidak dapat meminta informasi tambahan."

);


const afterFinishAnswer =

    citizenAnswer(

        aduan,

        "628123456789",

        "Jawaban setelah selesai."

    );


assert(

    afterFinishAnswer.success === false,

    "Aduan selesai tidak dapat menerima jawaban baru."

);


// ==========================================================
// TEST DASHBOARD
// ==========================================================

const dashboard =

    dashboardSummary(

        petugasOwner,

        [

            aduan,

            {

                ID: "ADU-20260721-0002",

                Status: "BARU",

                Owner: "PTG-002"

            }

        ]

    );


assert(

    dashboard.total === 1,

    "Dashboard hanya menghitung aduan milik petugas."

);


assert(

    dashboard.selesai === 1,

    "Dashboard menghitung aduan selesai dengan benar."

);


// ==========================================================
// SELESAI
// ==========================================================

console.log(`

==========================================================

🎉 SEMUA TEST BASELINE BERHASIL

==========================================================

`);