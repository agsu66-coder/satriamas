const petugasService = require("../services/petugasService");
const conversationService = require("../services/conversationService");
const aduanService = require("../services/aduanService");
const notificationService = require("../services/notificationService");

    // =====================================
    // Mengambil isi pesan yang direply
    // =====================================
    function getQuotedId(msg) {

        try {

             return msg._data?.quotedMsg?.id?._serialized
                || msg._data?.quotedStanzaID
                || null;

        } catch {

            return null;

        }

    }

    function extractComplaintId(text) {

        if (!text) return null;

        const match = text.match(/ADU-\d{8}-\d{4}/i);

        return match ? match[0].toUpperCase() : null;

    }
    // =====================================
    // Mengambil Nomor Aduan
    // =====================================


async function handlePetugas(client, msg) {

    const quotedText =
        msg._data?.quotedMsg?.body || "";

    const quotedAduanId =
        extractComplaintId(quotedText);
    const namaWA = msg._data.notifyName;
    const text = (msg.body || "").trim();

    console.log("=========== PETUGAS ===========");
    console.log("Nama WA :", namaWA);
    console.log("From :", msg.from);
    console.log("Notify :", msg._data.notifyName);
    console.log("Body :", text);
    console.log("Quoted :", quotedText);
    console.log("Aduan :", quotedAduanId);
    console.log("===============================");
    
    const session = conversationService.get(namaWA);

    
    // =====================================
    // Pastikan pengirim adalah petugas
    // =====================================

    const petugas =
        petugasService.getByName(namaWA);

    console.log("Petugas :", petugas);
    console.log(
        "Session :",
        session
    );

    if (!petugas) {

        return false;


    }
    // ====================================================
    // PETUGAS SEDANG MENULIS PERTANYAAN INFO
    // ====================================================

    if (session?.mode === "INFO") {

        const aduan = aduanService.getById(session.aduanId);

        if (!aduan) {

            conversationService.clear(namaWA);

            await msg.reply(
                "❌ Nomor aduan tidak ditemukan."
            );

            return true;

        }

        if (aduan.Status === "SELESAI") {

            conversationService.clear(namaWA);

            await msg.reply(
                "❌ Aduan ini sudah selesai."
            );

            return true;

        }

        if (Number(aduan.Jumlah_Info || 0) >= 3) {

            conversationService.clear(namaWA);

            await msg.reply(
                "❌ Permintaan informasi tambahan telah mencapai batas maksimal (3 kali)."
            );

            return true;

        }

        aduanService.increaseInfoCount(
            aduan.ID
        );

        aduanService.addInfoHistory(
            aduan.ID,
            text
        );
 
        aduanService.updateStatus(
            aduan.ID,
            "MENUNGGU_INFO"
        );

        await notificationService.sendInfoRequest(

            client,

            aduan,

            text

        );

        conversationService.clear(namaWA);

        await msg.reply(
            "✅ Permintaan informasi berhasil dikirim kepada pelapor."
        );

        return true;

    }

    // ====================================================
    // PETUGAS SEDANG MENULIS FEEDBACK
    // ====================================================

    if (session?.mode === "FEEDBACK") {

        const aduan = aduanService.getById(session.aduanId);

        if (!aduan) {

            conversationService.clear(namaWA);

            await msg.reply(
                "❌ Nomor aduan tidak ditemukan."
            );

            return true;

        }

        if (aduan.Status === "SELESAI") {

            conversationService.clear(namaWA);

            await msg.reply(
                "❌ Aduan sudah selesai sebelumnya."
            );

            return true;

        }

        aduanService.updateFeedback(

            aduan.ID,

            text

        );

        aduanService.updateStatus(

            aduan.ID,

            "SELESAI"

        );

        await notificationService.sendFeedback(

            client,

            aduanService.getById(
                aduan.ID
            ),


        );

        conversationService.clear(namaWA);

        await msg.reply(

            "✅ Aduan telah dinyatakan selesai dan feedback telah dikirim kepada pelapor."

        );

        return true;

    }

    // ====================================================
    // QUICK ACTION MELALUI REPLY
    // ====================================================

    console.log("hasQuotedMsg :", msg.hasQuotedMsg);
    console.log("quotedAduanId :", quotedAduanId);

    if (

        msg.hasQuotedMsg &&
        quotedAduanId 

    ) {

        const aduan = aduanService.getById(
            quotedAduanId
        );

        if (!aduan) {

            await msg.reply(
                "❌ Nomor aduan tidak ditemukan."
            );

            return true;

        }

        if (aduan.Status === "SELESAI") {

            await msg.reply(
            "❌ Aduan ini sudah selesai."
        );

        return true;

        }

        if (text === "1") {

            aduanService.updateStatus(

                quotedAduanId,

                "MENUNGGU_INFO"

            );

            conversationService.set(namaWA, {

                mode: "INFO",

                aduanId: quotedAduanId

            });

            await msg.reply(

            "Silakan tuliskan informasi yang ingin ditanyakan kepada pelapor."

           );

           return true;

        }

        if (text === "2") {

            aduanService.updateStatus(

                quotedAduanId,

                "DIPROSES"

            );

            conversationService.set(namaWA, {

                mode: "FEEDBACK",

                aduanId: quotedAduanId

           });

           await msg.reply(

            "Silakan tuliskan tindak lanjut atau feedback yang akan dikirim kepada pelapor."

           );

           return true;

         }

    }
    // ====================================================
    // PERINTAH INFO
    // ====================================================

    if (text.toUpperCase().startsWith("INFO ")) {

        const aduanId =
            text.substring(5).trim();

        const aduan =
            aduanService.getById(aduanId);

        if (!aduan) {

            await msg.reply(
                "❌ Nomor aduan tidak ditemukan."
            );

            return true;

        }

        if (aduan.Status === "SELESAI") {

            await msg.reply(
                "❌ Aduan ini sudah selesai."
            );

            return true;

        }

        if (Number(aduan.Jumlah_Info || 0) >= 3) {

            await msg.reply(
                "❌ Permintaan informasi tambahan sudah mencapai batas maksimal."
            );

            return true;

        }

        conversationService.set(namaWA, {

            mode: "INFO",

            aduanId

        });

        await msg.reply(

            "Silakan tuliskan informasi yang ingin ditanyakan kepada pelapor."

        );

        return true;

    }

    // ====================================================
    // PERINTAH SELESAIKAN
    // ====================================================

    if (text.toUpperCase().startsWith("SELESAIKAN ")) {

        const aduanId =
            text.substring(11).trim();

        const aduan =
            aduanService.getById(aduanId);

        if (!aduan) {

            await msg.reply(
                "❌ Nomor aduan tidak ditemukan."
            );

            return true;

        }

        if (aduan.Status === "SELESAI") {

            await msg.reply(
                "❌ Aduan sudah selesai sebelumnya."
            );

            return true;

        }

        conversationService.set(namaWA, {

            mode: "FEEDBACK",

            aduanId

        });

        await msg.reply(

            "Silakan tuliskan tindak lanjut yang akan dikirim kepada pelapor."

        );

        return true;

    }

    // ====================================================
    // Pesan lain dari petugas
    // ====================================================

    if (text === "1" || text === "2") {

        await msg.reply(

`⚠️ Untuk menjaga ketepatan penanganan aduan, silakan gunakan fitur *Balas (Reply)* pada pesan aduan dari TERATAI.

Langkahnya:

1️⃣ Balas pesan aduan

2️⃣ Ketik angka *1* untuk meminta informasi tambahan

3️⃣ Ketik angka *2* untuk menyelesaikan aduan`

        );

        return true;

    }
    await msg.reply(

`Perintah yang tersedia:

INFO <Nomor Aduan>

SELESAIKAN <Nomor Aduan>`

    );

    return true;

}

module.exports = {

    handlePetugas

};