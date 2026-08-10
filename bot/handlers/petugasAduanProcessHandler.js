const aduanService =
    require("../services/aduanService");

const conversationService =
    require("../services/conversationService");


// =====================================
// PROSES ADUAN PETUGAS
// =====================================

async function processAduan(client, msg) {

    const namaWA =
        msg._data?.notifyName;

    const text =
        (msg.body || "").trim();


    // =====================================
    // AMBIL SESSION
    // =====================================

    const session =
        conversationService.get(namaWA);


    // =====================================
    // VALIDASI SESSION
    // =====================================

    if (

        !session ||

        session.mode !== "ADUAN_PROCESS" ||

        !session.aduanId

    ) {

        return false;

    }


    // =====================================
    // AMBIL DATA ADUAN
    // =====================================

    const aduan =
        aduanService.getById(

            session.aduanId

        );


    if (!aduan) {

        conversationService.clear(namaWA);

        await msg.reply(

            "❌ Aduan tidak ditemukan."

        );

        return true;

    }


    // =====================================
    // VALIDASI STATUS
    // =====================================

    if (

        aduan.Status === "SELESAI"

    ) {

        conversationService.clear(namaWA);

        await msg.reply(

            "❌ Aduan ini sudah selesai dan tidak dapat diproses kembali."

        );

        return true;

    }


    // =====================================
    // PILIHAN PROSES
    // =====================================

    if (text === "1") {

        aduanService.updateStatus(

            aduan.ID,

            "DIPROSES"

        );


        conversationService.set(

            namaWA,

            {

                mode: "INFO",

                aduanId: aduan.ID

            }

        );


        await msg.reply(

`⚙️ *ADUAN SEDANG DIPROSES*

Nomor:
${aduan.ID}

Silakan tuliskan informasi tambahan yang ingin diminta kepada pelapor.`

        );


        return true;

    }


    // =====================================
    // SELESAIKAN ADUAN
    // =====================================

    if (text === "2") {

        aduanService.updateStatus(

            aduan.ID,

            "DIPROSES"

        );


        conversationService.set(

            namaWA,

            {

                mode: "FEEDBACK",

                aduanId: aduan.ID

            }

        );


        await msg.reply(

`⚙️ *PENYELESAIAN ADUAN*

Nomor:
${aduan.ID}

Silakan tuliskan tindak lanjut atau feedback yang akan dikirim kepada pelapor.`

        );


        return true;

    }


    // =====================================
    // KEMBALI KE DETAIL
    // =====================================

    if (text === "0") {

        conversationService.set(

            namaWA,

            {

                mode: "ADUAN_DETAIL",

                aduanId: aduan.ID

            }

        );


        await msg.reply(

`📄 *DETAIL ADUAN*

Nomor:
${aduan.ID}

Pelapor:
${aduan.Nama}

Tanggal:
${aduan.Tanggal}

Isi Aduan:
${aduan.Isi}

Status:
${aduan.Status}

Jumlah Informasi:
${aduan.Jumlah_Info || 0}

Tanggal Update:
${aduan.Tanggal_Update}

━━━━━━━━━━━━━━

1️⃣ Proses Aduan

0️⃣ Kembali`

        );


        return true;

    }


    // =====================================
    // INPUT TIDAK VALID
    // =====================================

    await msg.reply(

`❌ Pilihan tidak tersedia.

Silakan pilih:

1️⃣ Minta Informasi Tambahan

2️⃣ Selesaikan Aduan

0️⃣ Kembali`

    );


    return true;

}


module.exports = {

    processAduan

};