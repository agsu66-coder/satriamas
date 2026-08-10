const aduanService =
    require("../../bot/services/aduanService");

const OWNER = "PTG001";

console.log("================================");
console.log("TEST FILTER ADUAN");
console.log("OWNER :", OWNER);
console.log("================================");

const semua =
    aduanService.getByOwner(OWNER);

const baru =
    aduanService.getByOwnerAndStatus(
        OWNER,
        "BARU"
    );

const menungguInfo =
    aduanService.getByOwnerAndStatus(
        OWNER,
        "MENUNGGU_INFO"
    );

const diproses =
    aduanService.getByOwnerAndStatus(
        OWNER,
        "DIPROSES"
    );

const selesai =
    aduanService.getByOwnerAndStatus(
        OWNER,
        "SELESAI"
    );

console.log("\n=== RINGKASAN ===");

console.log({

    semua: semua.length,

    baru: baru.length,

    menungguInfo:
        menungguInfo.length,

    diproses:
        diproses.length,

    selesai:
        selesai.length

});

console.log("\n=== ID ADUAN OWNER ===");

console.log(

    semua.map(

        item => item.ID

    )

);

console.log("\n=== ID ADUAN BARU ===");

console.log(

    baru.map(

        item => item.ID

    )

);

console.log("\n=== ID MENUNGGU INFO ===");

console.log(

    menungguInfo.map(

        item => item.ID

    )

);

console.log("\n=== ID DIPROSES ===");

console.log(

    diproses.map(

        item => item.ID

    )

);

console.log("\n=== ID SELESAI ===");

console.log(

    selesai.map(

        item => item.ID

    )

);