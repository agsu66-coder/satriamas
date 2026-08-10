const petugas = require("./services/petugasService");

console.log("===== Semua Petugas =====");

console.log(

    petugas.getAll()

);

console.log();

console.log("===== KAT001 =====");

console.log(

    petugas.getByCategory("KAT001")

);

console.log();

console.log("===== Nomor =====");

console.log(

    petugas.exists("628123456789")

);