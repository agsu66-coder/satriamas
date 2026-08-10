const XLSX = require("xlsx");
const path = require("path");

const FILE = path.join(
    __dirname,
    "../../backend/database/TERATAI_CORE.xlsx"
);

const SHEET_AKTIVITAS = "AKTIVITAS";
const SHEET_ADUAN = "ADUAN";

class ReportService {

    // =====================================
    // LOAD WORKBOOK
    // =====================================

    loadWorkbook() {

        return XLSX.readFile(FILE);

    }

    // =====================================
    // AMBIL DATA SHEET
    // =====================================

    getSheetRecords(workbook, sheetName) {

        const sheet =
            workbook.Sheets[sheetName];

        if (!sheet) {

            return [];

        }

        return XLSX.utils.sheet_to_json(

            sheet

        );

    }

    // =====================================
    // PARSE TANGGAL
    // =====================================

    parseDate(value) {

        if (!value) {

            return null;

        }

        const date =
            new Date(value);

        if (

            Number.isNaN(

                date.getTime()

            )

        ) {

            return null;

        }

        return date;

    }

    // =====================================
    // FILTER PERIODE
    // =====================================

    filterByDate(

        records,

        tanggalMulai,

        tanggalAkhir,

        field

    ) {

        const mulai =
            this.parseDate(

                tanggalMulai

            );

        const akhir =
            this.parseDate(

                tanggalAkhir

            );

        if (!mulai || !akhir) {

            return records;

        }

        akhir.setHours(

            23,

            59,

            59,

            999

        );

        return records.filter(

            item => {

                const tanggal =
                    this.parseDate(

                        item[field]

                    );

                if (!tanggal) {

                    return false;

                }

                return (

                    tanggal >= mulai &&

                    tanggal <= akhir

                );

            }

        );

    }

    // =====================================
    // LAPORAN AKTIVITAS
    // =====================================

    getActivitySummary(

        tanggalMulai,

        tanggalAkhir

    ) {

        const workbook =
            this.loadWorkbook();

        const records =
            this.getSheetRecords(

                workbook,

                SHEET_AKTIVITAS

            );

        const filtered =
            this.filterByDate(

                records,

                tanggalMulai,

                tanggalAkhir,

                "Waktu"

            );

        const administrasi =
            filtered.filter(

                item =>

                    item.Kategori ===

                    "ADMINISTRASI"

            );

        const uniqueUsers =
            new Set(

                administrasi

                    .map(

                        item =>

                            item.User_Key

                    )

                    .filter(

                        value =>

                            value

                    )

            );

        return {

            totalAktivitas:

                filtered.length,

            totalPenggunaAdministrasi:

                uniqueUsers.size,

            totalSesiAdministrasi:

                administrasi.length

        };

    }

    // =====================================
    // LAPORAN ADUAN
    // =====================================

    getComplaintSummary(

        tanggalMulai,

        tanggalAkhir

    ) {

        const workbook =
            this.loadWorkbook();

        const records =
            this.getSheetRecords(

                workbook,

                SHEET_ADUAN

            );

        const filtered =
            this.filterByDate(

                records,

                tanggalMulai,

                tanggalAkhir,

                "Tanggal"

            );

        return {

            totalAduan:

                filtered.length,

            baru:

                filtered.filter(

                    item =>

                        item.Status ===

                        "BARU"

                ).length,

            diproses:

                filtered.filter(

                    item =>

                        item.Status ===

                        "DIPROSES"

                ).length,

            menungguInfo:

                filtered.filter(

                    item =>

                        item.Status ===

                        "MENUNGGU_INFO"

                ).length,

            selesai:

                filtered.filter(

                    item =>

                        item.Status ===

                        "SELESAI"

                ).length

        };

    }

    // =====================================
    // LAPORAN LENGKAP
    // =====================================

    getSummary(

        tanggalMulai,

        tanggalAkhir

    ) {

        return {

            periode: {

                mulai:

                    tanggalMulai,

                akhir:

                    tanggalAkhir

            },

            aktivitas:

                this.getActivitySummary(

                    tanggalMulai,

                    tanggalAkhir

                ),

            aduan:

                this.getComplaintSummary(

                    tanggalMulai,

                    tanggalAkhir

                )

        };

    }

}

module.exports =
    new ReportService();