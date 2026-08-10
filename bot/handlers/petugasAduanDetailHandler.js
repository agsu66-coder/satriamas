const aduanService =
    require("../services/aduanService");

const conversationService =
    require("../services/conversationService");


// =====================================
// HANDLER DETAIL ADUAN PETUGAS
// =====================================

async function processDetail(client, msg) {

    const namaWA =
        msg._data?.notifyName;

    const text =
        (msg.body || "").trim();


    // =================================
    // AMBIL SESSION
    // =================================

    const session =
        conversationService.get(namaWA);


    // =================================
    // BUKAN SESSION DETAIL
    // =================================

    if (

        !session ||

        session.mode !== "ADUAN_DETAIL"

    ) {

        return false;

    }


    // =================================
    // KEMBALI
    // =================================

    if (

        text === "0"

    ) {

        conversationService.set(

            namaWA,

            {

                mode: "DASHBOARD"

            }

        );


        await msg.reply(

`🌿 *DASHBOARD PETUGAS*

Silakan pilih menu:

1️⃣ Aduan Saya

2️⃣ Aduan Baru

3️⃣ Menunggu Informasi

4️⃣ Sedang Diproses

5️⃣ Riwayat Selesai

0️⃣ Keluar Dashboard`

        );

        return true;

    }


    // =================================
    // AMBIL ADUAN DARI SESSION
    // =================================

    const aduan =
        aduanService.getById(

            session.aduanId

        );


    if (!aduan) {

        await msg.reply(

`❌ Nomor aduan tidak ditemukan.

0️⃣ Kembali`

        );

        return true;

    }


    // =================================
    // VALIDASI OWNER
    // =================================

    if (

        aduan.Owner !== session.ownerId

    ) {

        await msg.reply(

            "❌ Aduan ini bukan tanggung jawab Anda."

        );

        return true;

    }


    // =================================
    // PILIHAN PROSES ADUAN
    // =================================

    if (

        text === "1"

    ) {

        conversationService.set(

            namaWA,

            {

                mode: "ADUAN_PROCESS",

                ownerId: session.ownerId,

                aduanId: aduan.ID

            }

        );


        await msg.reply(

`⚙️ *ADUAN SEDANG DIPROSES*

Nomor:

${aduan.ID}

Silakan pilih tindakan:

1️⃣ Minta informasi tambahan

2️⃣ Selesaikan aduan

0️⃣ Kembali`

        );

        return true;

    }


    // =================================
    // PILIHAN TIDAK VALID
    // =================================

    await msg.reply(

`❌ Pilihan tidak valid.

1️⃣ Proses Aduan

0️⃣ Kembali`

    );

    return true;

}


module.exports = {

    process: processDetail

};