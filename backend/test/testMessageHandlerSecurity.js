const messageHandler =
require("../../bot/handlers/messageHandler");

const stateService =
require("../../bot/services/stateService");

const aduanService =
require("../../bot/services/aduanService");

// =====================================
// MOCK CLIENT
// =====================================

const mockClient = {


async sendMessage(to, text) {

    console.log("\n===== MOCK SEND MESSAGE =====");

    console.log("KEPADA :", to);

    console.log("PESAN :");

    console.log(text);

    console.log("=============================\n");

}


};

// =====================================
// MOCK MESSAGE
// =====================================

function createMsg({


from,

notifyName,

body,

hasQuotedMsg = false,

quotedText = ""


}) {


return {

    from,

    body,

    fromMe: false,

    isStatus: false,

    hasQuotedMsg,

    _data: {

        notifyName,

        quotedMsg: hasQuotedMsg

            ? {

                body: quotedText

            }

            : null

    },

    replies: [],

    async reply(text) {

        console.log("\n===== BALASAN BOT =====");

        console.log(text);

        console.log("=======================\n");

        this.replies.push(text);

    }

};


}

// =====================================
// DATA WARGA
// =====================================

const WARGA_A =
"[6287736833184@c.us](mailto:6287736833184@c.us)";

const WARGA_B =
"[6281234567890@c.us](mailto:6281234567890@c.us)";

// =====================================
// TEST UTAMA
// =====================================

async function runTest() {


console.log("\n================================");

console.log(
    "TEST MESSAGE HANDLER - SECURITY"
);

console.log("================================");


// =================================
// SECURITY 1
// BUAT ADUAN MILIK WARGA A
// =================================

console.log(

    "\n=== SECURITY 1 : BUAT ADUAN WARGA A ==="

);


const aduanId =

    aduanService.create({

        No_WA:
            WARGA_A,

        Nama:
            "Warga A",

        Kategori_ID:
            "KAT001",

        Isi:
            "Aduan milik Warga A",

        Owner:
            "PTG001"

    });


aduanService.updateStatus(

    aduanId,

    "MENUNGGU_INFO"

);


aduanService.increaseInfoCount(

    aduanId

);


aduanService.addInfoHistory(

    aduanId,

    "Mohon kirimkan dokumen pendukung."

);


const aduanSebelum =

    aduanService.getById(

        aduanId

    );


const riwayatSebelum =

    aduanSebelum.Riwayat_Info;


console.log(

    "ADUAN ID :",

    aduanId

);


console.log(

    "PEMILIK :",

    aduanSebelum.No_WA

);


// =================================
// SECURITY 2
// WARGA B MENCOBA MEMBALAS
// =================================

console.log(

    "\n=== SECURITY 2 : WARGA B MENCOBA AKSES ADUAN WARGA A ==="

);


stateService.clearState(

    WARGA_B

);


const quotedText =


`📢 *Informasi Tambahan Dibutuhkan*

Nomor Aduan :

${aduanId}

Petugas meminta informasi berikut:

Mohon kirimkan dokumen pendukung.

Silakan balas pesan ini.`;


await messageHandler.handleMessage(

    mockClient,

    createMsg({

        from:
            WARGA_B,

        notifyName:
            "Warga B",

        body:
            "Ini jawaban dari Warga B.",

        hasQuotedMsg:
            true,

        quotedText

    })

);


// =================================
// SECURITY 3
// VERIFIKASI DATABASE
// =================================

console.log(

    "\n=== SECURITY 3 : VERIFIKASI DATA ==="

);


const aduanSesudah =

    aduanService.getById(

        aduanId

    );


const riwayatSesudah =

    aduanSesudah.Riwayat_Info;


if (

    riwayatSesudah ===

    riwayatSebelum

) {

    console.log(

        "✅ Riwayat aduan tidak berubah."

    );

}

else {

    console.error(

        "❌ SECURITY FAILURE: Riwayat aduan berubah!"

    );

}


if (

    aduanSesudah.No_WA ===

    WARGA_A

) {

    console.log(

        "✅ Pemilik aduan tetap benar."

    );

}

else {

    console.error(

        "❌ SECURITY FAILURE: Pemilik aduan berubah!"

    );

}


// =================================
// SECURITY 4
// PASTIKAN STATUS TETAP
// =================================

if (

    aduanSesudah.Status ===

    "MENUNGGU_INFO"

) {

    console.log(

        "✅ Status aduan tetap MENUNGGU_INFO."

    );

}

else {

    console.error(

        "❌ SECURITY FAILURE: Status aduan berubah!"

    );

}


console.log(

    "\n================================"

);

console.log(

    "TEST SECURITY SELESAI"

);

console.log(

    "================================"

);


}

// =====================================
// JALANKAN TEST
// =====================================

runTest()


.catch(err => {

    console.error(

        "TEST SECURITY ERROR:",

        err

    );

});

