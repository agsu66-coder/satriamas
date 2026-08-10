const XLSX = require("xlsx");
const path = require("path");

const FILE = path.join(
    __dirname,
    "../../backend/database/TERATAI_CORE.xlsx"
);

const SHEET = "PETUGAS_ADUAN";

class PetugasService {

    constructor() {

        this.reload();

    }

    // ============================
    // Reload Workbook
    // ============================

    reload() {

        const workbook = XLSX.readFile(FILE);

        const sheet = workbook.Sheets[SHEET];

        this.records = XLSX.utils.sheet_to_json(sheet);

        console.log("=== DATA PETUGAS ===");
        console.log(this.records[0]);
        console.log("====================");

    }

    // ============================
    // Semua Petugas Aktif
    // ============================

    getAll() {

        return this.records.filter(

            item =>

                String(item.Aktif).toUpperCase() === "YA"

        );

    }

    // ============================
    // Berdasarkan Kategori
    // ============================

    getByCategory(kategoriId) {

        return this.records.filter(

            item =>

                String(item.Aktif).toUpperCase() === "YA"

                &&

                item.Kategori_ID === kategoriId

        );

    }

    // ============================
    // Berdasarkan ID
    // ============================

    getById(id) {

        return this.records.find(

            item => item.ID === id

        );

    }

    // ============================
    // Berdasarkan Nomor WA
    // ============================

    getByWhatsapp(number) {

        return this.records.find(

            item =>

                String(item.Nomor_WA)

                    .replace(/\D/g, "")

                ===

                String(number)

                    .replace(/\D/g, "")

        );

    }

    // ============================
    // Apakah Nomor Petugas
    // ============================

    exists(number) {

        return this.getByWhatsapp(number) != null;

    }
    // ============================
    // Berdasarkan Nama WA
    // ============================

    getByName(name) {

        return this.records.find(item =>

            String(item.Aktif).toUpperCase() === "YA"

            &&

            String(item.Nama_WA || "")
                .trim()
                .toLowerCase()

            ===

            String(name || "")
                .trim()
                .toLowerCase()

        );

    }

    // ============================
    // Satu Petugas Berdasarkan Kategori
    // ============================

    getOwnerByCategory(kategoriId) {

        const hasil = this.records.filter(item =>

            String(item.Aktif).toUpperCase() === "YA"

            &&

            item.Kategori_ID === kategoriId

        );

        console.log("=== HASIL FILTER ===");
        console.log(hasil);
        console.log("Jumlah :", hasil.length);

        if (hasil.length === 0) {

            console.warn(
            `Kategori ${kategoriId} tidak memiliki petugas aktif.`
            );

            return null;

        }

        if (hasil.length > 1) {

            throw new Error(
            `Kategori ${kategoriId} memiliki lebih dari satu petugas aktif.`
            );

        }

        return hasil[0];
        

    }

    // ============================
    // Apakah Nama WA Petugas
    // ============================

    existsByName(name) {

        return this.getByName(name) != null;

    }

    }

const petugasService = new PetugasService();

module.exports = petugasService;