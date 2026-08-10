const stateService =
    require("./stateService");

const templateClient =
    require("./templateClient");


// ==========================================================
// PENYIMPAN TIMER ADMINISTRASI
// ==========================================================

const timers =
    new Map();


// ==========================================================
// MULAI TIMER ADMINISTRASI
// ==========================================================

function start(client, user) {

    // ------------------------------------------------------
    // HAPUS TIMER LAMA
    // ------------------------------------------------------

    clear(user);


    // ------------------------------------------------------
    // BUAT TIMER BARU
    // ------------------------------------------------------

    const timeout = setTimeout(

        async () => {

            try {

                // ==================================================
                // AMBIL PESAN PENUTUP DARI TERATAI CORE
                // ==================================================

                const pesan =

                    await templateClient.renderTemplate(

                        "ADMIN_TIMEOUT"

                    );


                // ==================================================
                // VALIDASI TEMPLATE
                // ==================================================

                if (

                    !pesan

                ) {

                    throw new Error(

                        "Template ADMIN_TIMEOUT kosong."

                    );

                }


                // ==================================================
                // KIRIM KE USER MENGGUNAKAN ID ASLI
                // ==================================================

                await client.sendMessage(

                    user,

                    pesan

                );


                console.log(

                    "[AdminTimeout] Pesan penutup berhasil dikirim."

                );

            }


            catch (err) {

                console.error(

                    "[AdminTimeout]",

                    err.message

                );

            }


            // ==================================================
            // BERSIHKAN STATE ADMINISTRASI
            // ==================================================

            stateService.clearState(

                user

            );


            // ==================================================
            // HAPUS TIMER
            // ==================================================

            timers.delete(

                user

            );

        },

        2 * 60 * 1000

    );


    // ==================================================
    // SIMPAN TIMER
    // ==================================================

    timers.set(

        user,

        timeout

    );

}


// ==========================================================
// HAPUS TIMER USER
// ==========================================================

function clear(user) {

    const timer =
        timers.get(user);


    if (

        timer

    ) {

        clearTimeout(

            timer

        );


        timers.delete(

            user

        );

    }

}


// ==========================================================
// HAPUS SEMUA TIMER
// ==========================================================

function clearAll() {

    for (

        const timer

        of timers.values()

    ) {

        clearTimeout(

            timer

        );

    }


    timers.clear();

}


// ==========================================================
// EXPORT
// ==========================================================

module.exports = {

    start,

    clear,

    clearAll

};