const kategori = require("./services/kategoriService");

console.log("===== Semua =====");

console.log(

    kategori.getAll()

);

console.log();

console.log("===== Menu 1 =====");

console.log(

    kategori.getByMenu("1")

);

console.log();

console.log("===== ID =====");

console.log(

    kategori.getById("KAT001")

);