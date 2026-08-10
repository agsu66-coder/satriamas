const menuHandler = require("./menuHandler");

const adminTimeoutService =
    require("../services/adminTimeoutService");

const stateService =
    require("../services/stateService");

const conversationService =
    require("../services/conversationService");

const aiClient =
    require("../services/aiClient");

const petugasService =
    require("../services/petugasService");

const petugasHandler =
    require("./petugasHandler");

const petugasMenuHandler =
    require("./petugasMenuHandler");

const petugasAduanDetailHandler =
    require("./petugasAduanDetailHandler");

const petugasAduanProcessHandler =
    require("./petugasAduanProcessHandler");

const complaintHandler =
    require("./citizen/complaintHandler");


// =====================================
// MESSAGE HANDLER UTAMA
// =====================================

async function handleMessage(client, msg) {

    try {

        // =====================================
        // ABAIKAN PESAN TERTENTU
        // =====================================

        if (

            msg.fromMe ||

            msg.isStatus ||

            msg.from.endsWith("@g.us")

        ) {

            return;

        }


        const text =
            (msg.body || "").trim();


        if (!text) {

            return;

        }


        const namaWA =
            msg._data?.notifyName;


        const petugas =
            petugasService.getByName(

                namaWA

            );


        const conversation =
            conversationService.get(

                namaWA

            );


        console.log("\n===== DEBUG MESSAGE ROUTER =====");

        console.log("FROM          :", msg.from);

        console.log("NAMA WA       :", namaWA);

        console.log("PETUGAS       :", petugas);

        console.log("CONVERSATION  :", conversation);

        console.log(

            "STATE WARGA    :",

            stateService.getState(msg.from)

        );

        console.log("================================\n");


        // =====================================
        // ROUTING PETUGAS
        // =====================================

        if (petugas) {

            // =================================
            // DASHBOARD RINGKASAN
            // =================================

            if (

                text.toUpperCase() === "DASHBOARD"

            ) {

                await petugasMenuHandler.processMenu(

                    client,

                    msg

                );

                return;

            }


            // =================================
            // INFO DAN FEEDBACK
            // =================================

            if (

                conversation?.mode === "INFO" ||

                conversation?.mode === "FEEDBACK"

            ) {

                await petugasHandler.handlePetugas(

                    client,

                    msg

                );

                return;

            }


            // =================================
            // QUICK ACTION MELALUI REPLY
            // =================================

            if (

                msg.hasQuotedMsg

            ) {

                await petugasHandler.handlePetugas(

                    client,

                    msg

                );

                return;

            }


            // =================================
            // PETUGAS TANPA SESSION
            // =================================

            await petugasHandler.handlePetugas(

                client,

                msg

            );

            return;

        }


        // =====================================
        // PETUGAS MEMBUKA DASHBOARD
        // =====================================

        if (

            petugas &&

            text.toUpperCase() === "DASHBOARD"

        ) {

            const handled =
                await petugasMenuHandler.processMenu(

                    client,

                    msg

                );

            if (handled) {

                return;

            }

        }


        // =====================================
        // ALUR WARGA
        // =====================================

        const handledComplaint =
            await complaintHandler.handle(

                client,

                msg

            );

        if (handledComplaint) {

            return;

        }


        // =====================================
        // AMBIL SESSION WARGA
        // =====================================

        const session =
            stateService.getState(

                msg.from

            );


        // =====================================
        // KLARIFIKASI ADMINISTRASI
        // =====================================
        //
        // State ini hanya aktif ketika
        // confidence = MEDIUM.
        //
        // Warga memilih:
        //
        // 1 = kandidat pertama
        // 2 = kandidat kedua
        // 0 = menjelaskan kembali
        //
        // =====================================

        if (

            session?.state ===
            "ADMIN_CLARIFICATION"

        ) {

            adminTimeoutService.clear(

                msg.from

            );


            const candidates =
                session.candidates || [];


            // =================================
            // PILIHAN 1
            // =================================

            if (

                text === "1"

            ) {

                if (!candidates[0]) {

                    await msg.reply(

                        "Pilihan informasi tidak tersedia.\n\n"
                        + "Silakan jelaskan kembali kebutuhan "
                        + "administrasi Anda."

                    );

                    stateService.setState(

                        msg.from,

                        {

                            state:
                                "ADMIN"

                        }

                    );

                    return;

                }


                const row =
                    candidates[0];


                const answer =
                    row.Jawaban || "";


                await msg.reply(

                    answer

                );


                // ---------------------------------
                // Setelah jawaban diberikan,
                // kembali ke alur konfirmasi lama.
                // ---------------------------------

                stateService.setState(

                    msg.from,

                    {

                        state:
                            "ADMIN_CONFIRM"

                    }

                );


                adminTimeoutService.start(

                    client,

                    msg.from

                );


                await msg.reply(

`Apakah masih ingin menggunakan layanan Administrasi?

1. Ya

0. Menu Utama`

                );


                return;

            }


            // =================================
            // PILIHAN 2
            // =================================

            if (

                text === "2"

            ) {

                if (!candidates[1]) {

                    await msg.reply(

                        "Pilihan informasi tidak tersedia.\n\n"
                        + "Silakan jelaskan kembali kebutuhan "
                        + "administrasi Anda."

                    );

                    stateService.setState(

                        msg.from,

                        {

                            state:
                                "ADMIN"

                        }

                    );

                    return;

                }


                const row =
                    candidates[1];


                const answer =
                    row.Jawaban || "";


                await msg.reply(

                    answer

                );


                // ---------------------------------
                // Setelah jawaban diberikan,
                // kembali ke alur konfirmasi lama.
                // ---------------------------------

                stateService.setState(

                    msg.from,

                    {

                        state:
                            "ADMIN_CONFIRM"

                    }

                );


                adminTimeoutService.start(

                    client,

                    msg.from

                );


                await msg.reply(

`Apakah masih ingin menggunakan layanan Administrasi?

1. Ya

0. Menu Utama`

                );


                return;

            }


            // =================================
            // PILIHAN 0
            // =================================

            if (

                text === "0"

            ) {

                stateService.setState(

                    msg.from,

                    {

                        state:
                            "ADMIN"

                    }

                );


                await msg.reply(

                    "Silakan jelaskan kembali "
                    + "kebutuhan administrasi Anda."

                );


                adminTimeoutService.start(

                    client,

                    msg.from

                );


                return;

            }


            // =================================
            // PILIHAN TIDAK VALID
            // =================================

            await msg.reply(

`Silakan pilih nomor sesuai pilihan Anda.

1. Informasi pertama
2. Informasi kedua
0. Jelaskan kembali kebutuhan Anda.`

            );


            adminTimeoutService.start(

                client,

                msg.from

            );


            return;

        }


        // =====================================
        // SESSION ADMINISTRASI
        // =====================================

        if (

            session?.state === "ADMIN"

        ) {

            const response =
                await aiClient.askAI(

                    text

                );


            // =================================
            // CONFIDENCE MEDIUM
            // =================================
            //
            // Jangan masuk ke ADMIN_CONFIRM.
            // Warga harus memilih kandidat dahulu.
            //
            // =================================

            if (

                response.method ===
                "confidence_medium"

            ) {

                stateService.setState(

                    msg.from,

                    {

                        state:
                            "ADMIN_CLARIFICATION",

                        candidates:
                            response.candidates || []

                    }

                );


                adminTimeoutService.start(

                    client,

                    msg.from

                );


                await msg.reply(

                    response.text

                );


                return;

            }


            // =================================
            // CONFIDENCE LOW
            // =================================
            //
            // Tidak memberikan jawaban FAQ.
            // Warga diarahkan ke Pengaduan.
            //
            // =================================

            if (

                response.method ===
                "confidence_low"

            ) {

                stateService.clearState(

                    msg.from

                );


                await msg.reply(

                    response.text

                );


                return;

            }


            // =================================
            // CONFIDENCE HIGH
            // =================================
            //
            // Ini adalah alur lama.
            // Tidak kita ubah.
            //
            // =================================

            await msg.reply(

                response.text

            );


            stateService.setState(

                msg.from,

                {

                    state:
                        "ADMIN_CONFIRM"

                }

            );


            adminTimeoutService.start(

                client,

                msg.from

            );


            await msg.reply(

`Apakah masih ingin menggunakan layanan Administrasi?

1. Ya

0. Menu Utama`

            );


            return;

        }

        // =====================================
        // SESSION ADMIN ACTIVE
        // =====================================

        if (

            session?.state === "ADMIN_ACTIVE"

        ) {

            const response =

                await aiClient.askAI(

                    text

                );


            // =================================
            // CONFIDENCE MEDIUM
            // =================================

            if (

                response.method ===
                "confidence_medium"

            ) {

                stateService.setState(

                    msg.from,

                    {

                        state:
                            "ADMIN_CLARIFICATION",

                        candidates:
                            response.candidates || []

                    }

                );


                adminTimeoutService.start(

                    client,

                    msg.from

                );


                await msg.reply(

                    response.text

                );


                return;

            }


            // =================================
            // CONFIDENCE LOW
            // =================================

            if (

                response.method ===
                "confidence_low"

            ) {

                stateService.clearState(

                    msg.from

                );


                await msg.reply(

                    response.text

                );


                return;

            }


            // =================================
            // CONFIDENCE HIGH
            // =================================

            await msg.reply(

                response.text

            );


            adminTimeoutService.start(

                client,

                msg.from

            );


            return;

        }


        // =====================================
        // KONFIRMASI ADMINISTRASI
        // =====================================

        if (

            session?.state === "ADMIN_CONFIRM"

        ) {

            adminTimeoutService.clear(

                msg.from

            );


            if (

                text === "1"

            ) {

                stateService.setState(

                    msg.from,

                    {

                        state: "ADMIN"

                    }

                );


                await msg.reply(

                    "Silakan tuliskan pertanyaan administrasi Anda."

                );

                return;

            }


            if (

                text === "0"

            ) {

                stateService.clearState(

                    msg.from

                );


                await msg.reply(

`🌿 SATRIA AI

Selamat datang di layanan SATRIA Kecamatan Binangun.

Silakan pilih menu:

1. Administrasi

2. Pengaduan`

                );


                return;

            }


            await msg.reply(

                "Silakan pilih 1 atau 0."

            );

            return;

        }


        // =====================================
        // MENU UTAMA
        // =====================================

        const handled =
            await menuHandler.processMenu(

                msg

            );

        if (handled) {

            return;

        }


        await msg.reply(

`🌿 *SATRIA BINANGUN*

Selamat datang di layanan SATRIA Kecamatan Binangun.

Silakan pilih menu:

1. Administrasi

2. Pengaduan

Ketik angka menu untuk melanjutkan.`

        );

    }

    catch (err) {

        console.error(err);


        await msg.reply(

            "⚠️ Terjadi kesalahan pada sistem. Silakan coba kembali beberapa saat lagi."

        );

    }

}


// =====================================
// EXPORT
// =====================================

module.exports = {

    handleMessage

};