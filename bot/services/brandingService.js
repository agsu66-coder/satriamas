const XLSX = require("xlsx");
const path = require("path");
const fs = require("fs");


// ==========================================================
// PATH TERATAI CORE
// ==========================================================

const FILE = path.join(

    __dirname,

    "../../backend/database/TERATAI_CORE.xlsx"

);


// ==========================================================
// NAMA SHEET KONFIGURASI
// ==========================================================

const SHEET = "KONFIGURASI";


// ==========================================================
// BRANDING SERVICE
// ==========================================================

class BrandingService {


    // ======================================================
    // LOAD KONFIGURASI
    // ======================================================

    loadConfiguration() {

        if (!fs.existsSync(FILE)) {

            throw new Error(

                `File TERATAI_CORE.xlsx tidak ditemukan:\n${FILE}`

            );

        }


        const workbook =

            XLSX.readFile(FILE);


        const sheet =

            workbook.Sheets[SHEET];


        if (!sheet) {

            throw new Error(

                `Sheet "${SHEET}" tidak ditemukan di TERATAI_CORE.xlsx.`

            );

        }


        const records =

            XLSX.utils.sheet_to_json(

                sheet,

                {

                    defval: ""

                }

            );


        const configuration = {};


        records.forEach(

            item => {


                const key =

                    String(

                        item.KEY || ""

                    )

                        .trim()

                        .toUpperCase();


                if (!key) {

                    return;

                }


                configuration[key] =

                    String(

                        item.VALUE || ""

                    )

                        .trim();

            }

        );


        return configuration;

    }


    // ======================================================
    // NORMALISASI PATH
    // ======================================================

    resolvePath(relativePath) {


        if (!relativePath) {

            return "";

        }


        const normalizedPath =

            String(

                relativePath

            )

                .trim()

                .replace(

                    /\\/g,

                    path.sep

                );


        return path.resolve(

            __dirname,

            "../../",

            normalizedPath

        );

    }


    // ======================================================
    // AMBIL BRANDING
    // ======================================================

    getBranding() {


        const config =

            this.loadConfiguration();


        const logoPath =

            this.resolvePath(

                config.LOGO_PATH

            );


        return {


            namaKabupaten:

                config.NAMA_KABUPATEN || "",


            namaInstansi:

                config.NAMA_INSTANSI || "",


            namaAplikasi:

                config.NAMA_APLIKASI || "",


            subjudulAplikasi:

                config.SUBJUDUL_APLIKASI || "",


            alamat:

                config.ALAMAT_INSTANSI || "",


            website:

                config.WEBSITE || "",


            telepon:

                config.TELEPON_INSTANSI || "",


            email:

                config.EMAIL_INSTANSI || "",


            logoPath

        };

    }


    // ======================================================
    // VALIDASI BRANDING
    // ======================================================

    validateBranding() {


        const branding =

            this.getBranding();


        const requiredFields = [

            "namaKabupaten",

            "namaInstansi",

            "namaAplikasi",

            "subjudulAplikasi"

        ];


        const missingFields =

            requiredFields.filter(

                field =>

                    !branding[field]

            );


        const logoExists =

            branding.logoPath

                ? fs.existsSync(

                    branding.logoPath

                )

                : false;


        return {


            valid:

                missingFields.length === 0 &&

                logoExists,


            missingFields,


            logoExists,


            branding

        };

    }

}


// ==========================================================
// EXPORT SINGLE INSTANCE
// ==========================================================

module.exports =

    new BrandingService();