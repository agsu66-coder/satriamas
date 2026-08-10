const aduan = require("./services/aduanService");

const id = aduan.create({

    No_WA: "628123456789",

    Nama: "Budi",

    Kategori_ID: "KAT001",

    Isi: "Jalan depan rumah rusak."

});

console.log("ID :", id);

console.log();

console.log(

    aduan.getById(id)

);

aduan.updateStatus(

    id,

    "DIPROSES"

);

console.log();

console.log(

    aduan.getById(id)

);