const stateService = require("../services/stateService");

const activityService =
    require("../services/activityService");

const kategoriService =
    require("../services/kategoriService");

const MENU = {
    KEMBALI: "0",
    ADMINISTRASI: "1",
    ADUAN: "2"
};

async function processMenu(msg) {

    const teks = (msg.body || "").trim();

    switch (teks) {

        case MENU.KEMBALI:

            stateService.clearState(msg.from);

            await msg.reply(
                "🏠 Kembali ke menu utama."
            );

            return true;

        case MENU.ADMINISTRASI:

            stateService.setState(msg.from, {

                state: "ADMIN"

            });    

            activityService.record({

                User_Key:
                    msg.from,

                Identity_Type:
                    msg.from.endsWith("@lid")
                        ? "LID"
                        : "PHONE",

                No_WA:
                    msg.from,

                Nama:
                    msg._data?.notifyName || "",

                Jenis_Aktivitas:
                    "AKSES_LAYANAN",

                Kategori:
                    "ADMINISTRASI",

                Referensi_ID:
                    ""

            });

            await msg.reply(
                "Silakan tuliskan pertanyaan administrasi Anda."
            );

            return true;
        case MENU.ADUAN:

            stateService.setState(

                msg.from,

                {

                    state: "PILIH_KATEGORI"

                }

            );

            await msg.reply(

                kategoriService.buildMenuText()

            );

            return true;

        default:

            return false;

    }

}

module.exports = {

    processMenu

};