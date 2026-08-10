const XLSX = require("xlsx");
const path = require("path");
const petugasService =
    require("./petugasService");
const STATUS = {

        BARU: "BARU",

        DIPROSES: "DIPROSES",

        MENUNGGU_INFO: "MENUNGGU_INFO",

        SELESAI: "SELESAI"

};
const FILE = path.join(
    __dirname,
    "../../backend/database/TERATAI_CORE.xlsx"
);

const SHEET = "ADUAN";

class AduanService {

    constructor() {

        this.reload();

    }

    // =========================
    // Reload Workbook
    // =========================

    reload() {

        this.workbook = XLSX.readFile(FILE);

        this.sheet = this.workbook.Sheets[SHEET];

        this.records = XLSX.utils.sheet_to_json(this.sheet);

    }

    // =========================
    // Simpan Workbook
    // =========================

    save() {

        this.workbook.Sheets[SHEET] =
            XLSX.utils.json_to_sheet(this.records);

        XLSX.writeFile(this.workbook, FILE);

    }

    // =========================
    // Semua Aduan
    // =========================

    getAll() {

        return this.records;

    }

    // =========================
    // Aduan Berdasarkan Owner
    // =========================

    getByOwner(ownerId) {

        return this.records.filter(

            item => item.Owner === ownerId

        );

    }


    // =========================
    // Aduan Berdasarkan Owner
    // dan Status
    // =========================

    getByOwnerAndStatus(ownerId, status) {

        return this.records.filter(

            item =>

                item.Owner === ownerId &&
                item.Status === status

        );

    }

    // =========================
    // Cari ID
    // =========================

    getById(id) {

        return this.records.find(

            item => item.ID === id

        );

    }

    // =========================
    // Generate Nomor Aduan
    // =========================

    generateId() {

        const now = new Date();

        const tanggal =
            now.getFullYear().toString() +
            String(now.getMonth() + 1).padStart(2, "0") +
            String(now.getDate()).padStart(2, "0");

        const prefix = `ADU-${tanggal}-`;

        const hariIni = this.records.filter(

            item => item.ID.startsWith(prefix)

        );

        const nomor =
            String(hariIni.length + 1).padStart(4, "0");

        return prefix + nomor;

    }

    // =========================
    // Tambah Aduan
    // =========================
    
    create(data) {
        const id = this.generateId();

        const now = this.getCurrentDateTime();

        this.records.push({

            ID: id,

            Tanggal: now,

            No_WA: data.No_WA,

            Nama: data.Nama,

            Kategori_ID: data.Kategori_ID,

            Isi: data.Isi,

            Status: STATUS.BARU,

            Owner: data.Owner || "",

            Feedback: "",
            
            Jumlah_Info: 0,

            Riwayat_Info: "",

            Tanggal_Update: now

        });

        this.save();

        return id;

    }

    // =========================
    // Create Complaint
    // =========================

    createComplaint(data) {

        const owner =
            petugasService.getOwnerByCategory(data.Kategori_ID);

        if (!owner) {

            throw new Error(
            "Belum ada petugas pada kategori tersebut."
            );

        }

        return this.create({

            ...data,

            Owner: owner.ID

        });

    }


    // =========================
    // Waktu Indonesia (WIB)
    // =========================

    getCurrentDateTime() {

    const now = new Date();

    const formatter = new Intl.DateTimeFormat("sv-SE", {

        timeZone: "Asia/Jakarta",

        year: "numeric",

        month: "2-digit",

        day: "2-digit",

        hour: "2-digit",

        minute: "2-digit",

        second: "2-digit",

        hour12: false

    });

    const parts = formatter.formatToParts(now);

    const data = {};

    parts.forEach(part => {

        if (part.type !== "literal") {

            data[part.type] = part.value;

        }

    });

    return `${data.year}-${data.month}-${data.day} ${data.hour}:${data.minute}:${data.second}`;

}



    

    // =========================
    // Update Status
    // =========================

    updateStatus(id, status) {

        const item = this.getById(id);

        if (!item) return false;

        item.Status = status;

        item.Tanggal_Update = this.getCurrentDateTime();

        this.save();

        return true;

    }

    // =========================
    // Update Owner
    // =========================

    updateOwner(id, owner) {

        const item = this.getById(id);

        if (!item) return false;

        item.Owner = owner;

        item.Tanggal_Update = this.getCurrentDateTime();

        this.save();

        return true;

    }

    // =========================
    // Update Feedback
    // =========================

    updateFeedback(id, feedback) {

        const item = this.getById(id);

        if (!item) return false;

        item.Feedback = feedback;

        item.Tanggal_Update = this.getCurrentDateTime();

        this.save();

        return true;

    }
    // =========================
    // Tambah Jumlah Info
    // =========================

    increaseInfoCount(id) {

        const item = this.getById(id);

        if (!item) return false;

        item.Jumlah_Info = Number(item.Jumlah_Info || 0) + 1;

        item.Tanggal_Update = this.getCurrentDateTime();

        this.save();

        return item.Jumlah_Info;

    }

// =========================
// Update Jawaban Warga
// =========================

updateLastAnswer(id, jawaban) {

    const item = this.getById(id);

    if (!item) return false;

    const history =
        item.Riwayat_Info || "";

    // =====================================
    // Ambil blok INFO terakhir
    // =====================================

    const infoMatches =
        history.match(/\[INFO-\d+\]/g);

    if (!infoMatches || infoMatches.length === 0) {

        return false;

    }

    const lastInfo =
        infoMatches[infoMatches.length - 1];

    const lastInfoIndex =
        history.lastIndexOf(lastInfo);

    const lastInfoBlock =
        history.substring(lastInfoIndex);

    // =====================================
    // Cegah jawaban ganda
    // =====================================

    if (

        lastInfoBlock.includes(
            "Jawaban Warga :"
        )

    ) {

        return false;

    }

    // =====================================
    // Tambahkan jawaban
    // =====================================

    item.Riwayat_Info =
`${history}

Jawaban Warga :
${jawaban}`.trim();

    item.Tanggal_Update =
        this.getCurrentDateTime();

    this.save();

    return true;

}

    // =========================
    // Tambah Riwayat Informasi
    // =========================

    addInfoHistory(id, pertanyaan) {

        const item = this.getById(id);

        if (!item) return false;

        const nomor = Number(item.Jumlah_Info || 0);

        const history = item.Riwayat_Info || "";

item.Riwayat_Info =
`${history}

[INFO-${nomor}]
Petugas :
${pertanyaan}`.trim();

        item.Tanggal_Update = this.getCurrentDateTime();

        this.save();

        return true;

    }

}

module.exports = new AduanService();
module.exports.exports = new AduanService();
