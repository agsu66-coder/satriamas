const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const config = require("./config/config");
const messageHandler = require("./handlers/messageHandler");


// ==================================================
// SYSTEM STATE
// ==================================================

let shuttingDown = false;


// ==================================================
// MEMBUAT CLIENT WHATSAPP
// ==================================================

const client = new Client({

    authStrategy: new LocalAuth({

        clientId: config.CLIENT_ID

    }),

    puppeteer: {

        executablePath: config.CHROME_PATH,

        args: [

            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process', // Opsional jika diperlukan di cloud
            '--disable-gpu',
            '--disable-setuid-sandbox'

        ]

    }

});


// ==================================================
// QR CODE
// ==================================================

client.on("qr", (qr) => {

    if (shuttingDown) {

        return;

    }

    console.clear();

    qrcode.generate(

        qr,

        {

            small: true

        }

    );

});


// ==================================================
// BOT SIAP
// ==================================================

client.on("ready", () => {

    if (shuttingDown) {

        return;

    }

    console.clear();

    console.log(

        "===================================="

    );

    console.log(

        "🌿 TERATAI AI"

    );

    console.log(

        "Asisten Digital Kecamatan Binangun"

    );

    console.log(

        "Status : ONLINE"

    );

    console.log(

        "===================================="

    );

});


// ==================================================
// SEMUA PESAN DITERUSKAN KE MESSAGE HANDLER
// ==================================================

client.on(

    "message",

    async (msg) => {

        // ------------------------------------------
        // CEK SHUTDOWN
        // ------------------------------------------

        if (shuttingDown) {

            console.log(

                "[SYSTEM] Bot sedang shutdown."

            );

            console.log(

                "[SYSTEM] Pesan baru diabaikan."

            );

            return;

        }

        // ------------------------------------------
        // PROSES PESAN
        // ------------------------------------------

        try {

            await messageHandler.handleMessage(

                client,

                msg

            );

        } catch (err) {

            console.error(

                "[BOT ERROR]",

                err

            );

        }

    }

);


// ==================================================
// GRACEFUL SHUTDOWN
// ==================================================

async function gracefulShutdown(

    signal

) {

    // ----------------------------------------------
    // CEGAH SHUTDOWN GANDA
    // ----------------------------------------------

    if (shuttingDown) {

        return;

    }

    // ----------------------------------------------
    // AKTIFKAN MODE SHUTDOWN
    // ----------------------------------------------

    shuttingDown = true;

    console.log(

        `\n[SYSTEM] Menerima ${signal}.`

    );

    console.log(

        "[SYSTEM] Menghentikan penerimaan pesan baru."

    );

    try {

        // ------------------------------------------
        // HENTIKAN CLIENT WHATSAPP
        // ------------------------------------------

        await client.destroy();

        console.log(

            "[SYSTEM] WhatsApp Bot berhasil dihentikan."

        );

    } catch (error) {

        console.error(

            "[SYSTEM] Error saat menghentikan Bot:",

            error.message

        );

    }

    // ----------------------------------------------
    // KELUAR DARI PROSES
    // ----------------------------------------------

    process.exit(

        0

    );

}


// ==================================================
// SIGNAL HANDLER
// ==================================================

process.on(

    "SIGINT",

    () => {

        gracefulShutdown(

            "SIGINT"

        );

    }

);


process.on(

    "SIGTERM",

    () => {

        gracefulShutdown(

            "SIGTERM"

        );

    }

);


// ==================================================
// JALANKAN BOT
// ==================================================

client.initialize();