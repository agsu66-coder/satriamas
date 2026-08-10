const petugasService =
    require("./petugasService");

const conversationService =
    require("./conversationService");

const templateClient =
    require("./templateClient");


class NotificationService {


    // ===================================
    // Normalisasi Nomor WhatsApp
    // ===================================

    normalize(number) {

        if (!number) {

            throw new Error(
                "Nomor WhatsApp kosong."
            );

        }

        let nomor =
            String(number)
                .replace(/\D/g, "");


        if (
            nomor.startsWith("0")
        ) {

            nomor =
                "62"
                +
                nomor.substring(1);

        }


        if (
            !nomor.endsWith("@c.us")
        ) {

            nomor += "@c.us";

        }


        return nomor;

    }


    // ===================================
    // Kirim 1 Pesan
    // ===================================

    async sendMessage(

        client,

        number,

        message

    ) {

        try {

            const chatId =
                this.normalize(number);


            console.log(
                "SEND :",
                chatId
            );


            const sent =
                await client.sendMessage(

                    chatId,

                    message

                );


            console.log(
                "BERHASIL"
            );


            return sent;

        }


        catch (err) {

            console.error(err);

            return false;

        }

    }


    // ===================================
    // Kirim ke Banyak Petugas
    // ===================================

    async sendToPetugas(

        client,

        daftarPetugas,

        message,

        aduanId = null

    ) {

        const hasil = [];


        for (

            const petugas
            of daftarPetugas

        ) {


            const sukses =
                await this.sendMessage(

                    client,

                    petugas.Nomor_WA,

                    message

                );


            if (

                sukses
                &&
                aduanId

            ) {


                conversationService.set(

                    petugas.Nomor_WA,

                    {

                        mode:
                            "MENU_ADUAN",

                        aduanId

                    }

                );

            }


            hasil.push({

                id:
                    petugas.ID,

                nama:
                    petugas.Nama,

                sukses:
                    !!sukses

            });

        }


        return hasil;

    }


    // ===================================
    // Aduan Baru
    // ===================================

    async sendNewComplaint(

        client,

        aduan,

        kategoriNama

    ) {


        const pesan =

`📢 *Aduan Baru*

Nomor :
${aduan.ID}

Kategori :
${kategoriNama}

Pelapor :
${aduan.Nama}

Isi Aduan :
${aduan.Isi}

Balas:

1. INFO ${aduan.ID}

2. SELESAIKAN ${aduan.ID}

━━━━━━━━━━━━━━

💡 Disarankan menggunakan fitur Reply.`;


        await this.sendToOwner(

            client,

            aduan,

            pesan

        );

    }


    // ===================================
    // Kirim ke Owner Aduan
    // ===================================

    async sendToOwner(

        client,

        aduan,

        message

    ) {


        console.log(
            "===== OWNER ====="
        );


        console.log(
            aduan
        );


        console.log(
            "Owner :",
            aduan.Owner
        );


        console.log(
            "================="
        );


        const owner =
            petugasService.getById(

                aduan.Owner

            );


        if (!owner) {


            console.log(
                "Owner tidak ditemukan."
            );


            return false;

        }


        const sukses =
            await this.sendMessage(

                client,

                owner.Nomor_WA,

                message

            );


        if (sukses) {


            conversationService.set(

                owner.Nama_WA,

                {

                    mode:
                        "MENU_ADUAN",

                    aduanId:
                        aduan.ID

                }

            );

        }


        return sukses;

    }


    // ===================================
    // Permintaan Informasi Tambahan
    // ===================================

    async sendInfoRequest(

        client,

        aduan,

        pertanyaan

    ) {


        const pesan =

`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :
${aduan.ID}

Petugas meminta informasi berikut:

${pertanyaan}

Silakan balas pesan ini.`;


        await this.sendMessage(

            client,

            aduan.No_WA,

            pesan

        );

    }


    // ===================================
    // Jawaban Warga
    // ===================================

    async sendCitizenAnswer(

        client,

        aduan

    ) {


        const pesan =

`📢 *Jawaban Pelapor*

Nomor :
${aduan.ID}

Isi Aduan:

${aduan.Isi}

Riwayat:

${aduan.Riwayat_Info}

Balas:

1. INFO ${aduan.ID}

2. SELESAIKAN ${aduan.ID}

━━━━━━━━━━━━━━

💡 Disarankan menggunakan fitur *Balas (Reply)* pada pesan ini.

Kemudian cukup kirim:

1 → Meminta informasi tambahan

2 → Menyelesaikan aduan`;


        await this.sendToOwner(

            client,

            aduan,

            pesan

        );

    }


    // ===================================
    // Feedback Penyelesaian
    // ===================================

    async sendFeedback(

        client,

        aduan

    ) {


        try {


            // ===================================
            // AMBIL TEMPLATE DARI BACKEND
            // ===================================

            const pesan =

                await templateClient.renderTemplate(

                    "ADUAN_FEEDBACK",

                    {

                        aduan_id:
                            aduan.ID,

                        feedback:
                            aduan.Feedback

                    }

                );


            // ===================================
            // DEBUG
            // ===================================

            console.log(
                "===== FEEDBACK TEMPLATE ====="
            );


            console.log(
                pesan
            );


            console.log(
                "============================="
            );


            // ===================================
            // KIRIM KE WARGA
            // ===================================

            return await this.sendMessage(

                client,

                aduan.No_WA,

                pesan

            );

        }


        catch (err) {


            console.error(

                "❌ GAGAL MENGAMBIL TEMPLATE FEEDBACK"

            );


            console.error(

                err.message

            );


            return false;

        }

    }


}


// ===================================
// EXPORT
// ===================================

module.exports =
    new NotificationService();