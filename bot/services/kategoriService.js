const XLSX = require("xlsx");
const path = require("path");

const FILE = path.join(
    __dirname,
    "../../backend/database/TERATAI_CORE.xlsx"
);

const SHEET = "KATEGORI_ADUAN";

class KategoriService {

    constructor() {

        this.reload();

    }

    // ==========================
    // Reload Workbook
    // ==========================

    reload() {

        const workbook = XLSX.readFile(FILE);

        const sheet = workbook.Sheets[SHEET];

        this.records = XLSX.utils.sheet_to_json(sheet);

    }

    // ==========================
    // Semua kategori aktif
    // ==========================

    getAll() {

        console.log(
            "KATEGORI:",
            this.records);

        return this.records.filter(

            item =>

                String(item.Aktif).toUpperCase() === "YA"

        );

    }

    // ==========================
    // Berdasarkan ID
    // ==========================

    getById(id) {

        return this.records.find(

            item => item.ID === id

        );

    }

    // ==========================
    // Berdasarkan Nomor Menu
    // ==========================

    getByMenu(menuNumber) {

        const kategori = this.getAll();

        const index = Number(menuNumber) - 1;

        if (index < 0 || index >= kategori.length) {

            return null;

        }

        return kategori[index];

    }

    // ==========================
    // Generate Menu WhatsApp
    // ==========================

    buildMenuText() {

        const kategori =
            this.getAll();

        let text =
    `📋 *Kategori Pengaduan*

    `;

        kategori.forEach(

            (item, index) => {

                text +=

    `${index + 1}. ${item.Nama_Kategori}

`    ;

            }

        );

        text +=

    "Balas dengan nomor kategori.";

        return text;

    }

}

module.exports = new KategoriService();