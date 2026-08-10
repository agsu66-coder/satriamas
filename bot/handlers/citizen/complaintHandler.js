
const stateService =
    require("../../services/stateService");

const kategoriService =
    require("../../services/kategoriService");

const aduanService =
    require("../../services/aduanService");

const notificationService =
    require("../../services/notificationService");


// =====================================
// EXTRACT NOMOR ADUAN
// =====================================

function extractComplaintId(text) {

    if (!text) return null;

    const match =
        text.match(/ADU-\d{8}-\d{4}/i);

    return match
        ? match[0].toUpperCase()
        : null;

}


// =====================================
// HANDLER PENGADUAN WARGA
// =====================================

async function handle(client, msg) {

    console.log(
        "========== COMPLAINT HANDLER DIPANGGIL =========="
    );

    console.log(
        "msg.from:",
        msg.from
    );

    console.log(
        "msg.hasQuotedMsg:",
        msg.hasQuotedMsg
    );

    console.log(
        "msg._data.quotedStanzaID:",
        msg._data?.quotedStanzaID
    );

    console.log(
        "msg._data.quotedMsg:",
        msg._data?.quotedMsg
    );

    console.log(
        "quoted body:",
        msg._data?.quotedMsg?.body
    );

    console.log(
        "================================================="
    );


    const text =
        (msg.body || "").trim();


    const quotedText =
        msg._data?.quotedMsg?.body || "";


    const aduanId =
        extractComplaintId(quotedText);


    // =====================================
    // BALASAN INFORMASI TAMBAHAN WARGA
    // =====================================

    if (

        msg.hasQuotedMsg &&
        aduanId

    ) {


        // =====================================
        // AMBIL DATA ADUAN
        // =====================================

        const aduan =
            aduanService.getById(

                aduanId

            );


        // =====================================
        // VALIDASI NOMOR ADUAN
        // =====================================

        if (!aduan) {

            await msg.reply(

                "❌ Nomor aduan tidak ditemukan."

            );

            return true;

        }


        // =====================================
        // HANYA PROSES JIKA MENUNGGU INFO
        // =====================================

        if (

            aduan.Status !== "MENUNGGU_INFO"

        ) {

            return false;

        }


        // =====================================
        // VALIDASI ADUAN SELESAI
        // =====================================

        if (

            aduan.Status === "SELESAI"

        ) {

            await msg.reply(

                "❌ Aduan ini sudah selesai."

            );

            return true;

        }


        // =====================================
        // AMBIL IDENTITAS KONTAK SEBENARNYA
        // =====================================

        let contactId;


        try {

            const contact =
                await msg.getContact();


            contactId =
                contact.id?._serialized;


            console.log(
                "========== DEBUG IDENTITAS SAAT BALAS =========="
            );

            console.log(
                "msg.from       :",
                msg.from
            );

            console.log(
                "contact.id     :",
                contactId
            );

            console.log(
                "contact.number :",
                contact.number
            );

            console.log(
                "No_WA aduan    :",
                aduan.No_WA
            );

            console.log(
                "================================================="
            );

        }

        catch (err) {

            console.error(

                "Gagal membaca identitas kontak:",

                err.message

            );

        }


        // =====================================
        // VALIDASI PEMILIK ADUAN
        // =====================================

        if (

            !contactId ||

            aduan.No_WA !== contactId

        ) {

            await msg.reply(

                "❌ Anda tidak memiliki akses terhadap aduan ini."

            );

            return true;

        }


        // =====================================
        // SIMPAN JAWABAN WARGA
        // =====================================

        const updated =
            aduanService.updateLastAnswer(

                aduanId,

                text

            );


        // =====================================
        // CEGAH JAWABAN GANDA
        // =====================================

        if (!updated) {

            await msg.reply(

`ℹ️ Jawaban untuk permintaan informasi terakhir telah diterima sebelumnya.

Silakan menunggu tindak lanjut petugas.`

            );

            return true;

        }


        // =====================================
        // AMBIL DATA TERBARU
        // =====================================

        const updatedAduan =
            aduanService.getById(

                aduanId

            );


        // =====================================
        // KIRIM JAWABAN KE PETUGAS
        // =====================================

        await notificationService
            .sendCitizenAnswer(

                client,

                updatedAduan

            );


        // =====================================
        // KONFIRMASI KE WARGA
        // =====================================

        await msg.reply(

`✅ Terima kasih.

Informasi Anda telah diteruskan kepada petugas.`

        );


        return true;

    }


    // =====================================
    // AMBIL SESSION WARGA
    // =====================================

    const session =
        stateService.getState(

            msg.from

        );


    // =====================================
    // TIDAK ADA SESSION
    // =====================================

    if (!session) {

        return false;

    }


    // =====================================
    // MENULIS ADUAN
    // =====================================

    if (

        session.state === "TULIS_ADUAN"

    ) {


        let nomorWA;


        // =====================================
        // AMBIL NOMOR WA
        // =====================================

        try {


            const contact =
                await msg.getContact();


            nomorWA =
                contact.id?._serialized

                ||

                msg.from;


            console.log(
                "========== DEBUG IDENTITAS SAAT BUAT ADUAN =========="
            );

            console.log(
                "msg.from              :",
                msg.from
            );

            console.log(
                "contact.id            :",
                contact.id?._serialized
            );

            console.log(
                "contact.number        :",
                contact.number
            );

            console.log(
                "nomorWA YANG DISIMPAN :",
                nomorWA
            );

            console.log(
                "======================================================"
            );

        }

        catch (err) {


            nomorWA =
                msg.from;


        }


        let id;


        // =====================================
        // BUAT ADUAN
        // =====================================

        try {


            id =
                aduanService.createComplaint({

                    No_WA:
                        nomorWA,

                    Nama:
                        msg._data?.notifyName

                        ||

                        "Masyarakat",

                    Kategori_ID:
                        session.kategori,

                    Isi:
                        text

                });


        }

        catch (err) {


            await msg.reply(

                err.message

            );


            return true;

        }


        // =====================================
        // AMBIL DATA ADUAN
        // =====================================

        const aduan =
            aduanService.getById(

                id

            );


        // =====================================
        // NOTIFIKASI PETUGAS
        // =====================================

        await notificationService
            .sendNewComplaint(

                client,

                aduan,

                session.kategoriNama

            );


        // =====================================
        // KONFIRMASI KE WARGA
        // =====================================

        await msg.reply(

`✅ Aduan berhasil diterima.

Nomor Tiket:
*${id}*

Terima kasih. Aduan Anda telah tercatat dalam sistem.`

        );


        // =====================================
        // HAPUS SESSION
        // =====================================

        stateService.clearState(

            msg.from

        );


        return true;

    }


    // =====================================
    // MEMILIH KATEGORI PENGADUAN
    // =====================================

    if (

        session.state === "PILIH_KATEGORI"

    ) {


        const kategori =
            kategoriService.getByMenu(

                text

            );


        // =====================================
        // KATEGORI TIDAK VALID
        // =====================================

        if (!kategori) {

            await msg.reply(

                "❌ Nomor kategori tidak tersedia.\n" +

                "Silakan pilih sesuai daftar."

            );

            return true;

        }


        // =====================================
        // SIMPAN KATEGORI
        // =====================================

        stateService.setState(

            msg.from,

            {

                state:
                    "TULIS_ADUAN",

                kategori:
                    kategori.ID,

                kategoriNama:
                    kategori.Nama_Kategori

            }

        );


        // =====================================
        // KONFIRMASI KATEGORI
        // =====================================

        await msg.reply(

`Kategori dipilih:
*${kategori.Nama_Kategori}*

Silakan tuliskan aduan Anda.`

        );


        return true;

    }


    // =====================================
    // TIDAK ADA ALUR YANG SESUAI
    // =====================================

    return false;

}


// =====================================
// EXPORT
// =====================================

module.exports = {

    handle

};

