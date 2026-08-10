const notificationService =
    require("../../bot/services/notificationService");

// ==========================================================
// MOCK CLIENT WHATSAPP
// ==========================================================

const mockClient = {

    async sendMessage(chatId, message) {

        console.log("");
        console.log("📤 MOCK WHATSAPP");
        console.log("Tujuan :", chatId);
        console.log("Pesan  :");
        console.log("------------------------------------------");
        console.log(message);
        console.log("------------------------------------------");

        return {

            id: "MOCK_MESSAGE_ID",

            to: chatId,

            body: message

        };

    }

};


// ==========================================================
// DATA ADUAN
// ==========================================================

const aduan = {

    ID:
        "ADU-20260722-INTEGRASI",

    No_WA:
        "628999999999@c.us",

    Nama:
        "Warga Test Integrasi",

    Feedback:
        "Aduan telah ditindaklanjuti melalui proses pelayanan."

};


// ==========================================================
// TEST
// ==========================================================

async function runTest() {

    console.log("");
    console.log(
        "=========================================================="
    );

    console.log(
        "🧪 TEST INTEGRASI NOTIFICATION FEEDBACK"
    );

    console.log(
        "=========================================================="
    );

    console.log("");

    console.log(
        "📤 Menjalankan notificationService.sendFeedback()..."
    );

    console.log("");

    const hasil =
        await notificationService.sendFeedback(

            mockClient,

            aduan

        );


    // ======================================================
    // VALIDASI HASIL
    // ======================================================

    if (!hasil) {

        throw new Error(

            "notificationService gagal mengirim feedback."

        );

    }


    console.log("");

    console.log(
        "✅ LULUS: notificationService berhasil mengambil template."
    );

    console.log(
        "✅ LULUS: Template ADUAN_FEEDBACK berhasil dirender."
    );

    console.log(
        "✅ LULUS: Pesan feedback berhasil dikirim."
    );


    console.log("");

    console.log(
        "=========================================================="
    );

    console.log(
        "🎉 TEST INTEGRASI NOTIFICATION FEEDBACK BERHASIL"
    );

    console.log(
        "=========================================================="
    );

}


runTest()

    .catch(err => {

        console.error("");

        console.error(
            "❌ TEST GAGAL"
        );

        console.error(
            err.message
        );

        process.exit(1);

    });