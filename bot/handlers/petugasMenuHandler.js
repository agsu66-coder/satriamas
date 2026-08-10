const petugasService =
    require("../services/petugasService");

const aduanService =
    require("../services/aduanService");


// =====================================
// DASHBOARD RINGKASAN PETUGAS
// =====================================

async function processMenu(client, msg) {

    const namaWA =
        msg._data?.notifyName;

    const text =
        (msg.body || "").trim();


    // =====================================
    // VALIDASI PERINTAH DASHBOARD
    // =====================================

    if (

        text.toUpperCase() !== "DASHBOARD"

    ) {

        return false;

    }


    // =====================================
    // VALIDASI PETUGAS
    // =====================================

    const petugas =
        petugasService.getByName(namaWA);


    if (!petugas) {

        return false;

    }


    // =====================================
    // AMBIL SEMUA ADUAN MILIK PETUGAS
    // =====================================

    const aduan =
        aduanService.getByOwner(

            petugas.ID

        );


    // =====================================
    // HITUNG RINGKASAN
    // =====================================

    const total =
        aduan.length;


    const baru =
        aduan.filter(

            item => item.Status === "BARU"

        ).length;


    const diproses =
        aduan.filter(

            item => item.Status === "DIPROSES"

        ).length;


    const menungguInfo =
        aduan.filter(

            item => item.Status === "MENUNGGU_INFO"

        ).length;


    const selesai =
        aduan.filter(

            item => item.Status === "SELESAI"

        ).length;


    // =====================================
    // KIRIM RINGKASAN
    // =====================================

    await msg.reply(

`🌿 *DASHBOARD PETUGAS*

Selamat datang, ${petugas.Nama}.

📊 *RINGKASAN ADUAN ANDA*

📋 Total Aduan        : ${total}

📢 Aduan Baru         : ${baru}

⚙️ Sedang Diproses    : ${diproses}

⏳ Menunggu Informasi : ${menungguInfo}

✅ Selesai            : ${selesai}`

    );


    return true;

}


module.exports = {

    processMenu

};