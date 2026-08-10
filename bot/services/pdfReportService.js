const PDFDocument = require("pdfkit");
const fs = require("fs");
const path = require("path");

const brandingService =
    require("./brandingService");

const reportService =
    require("./reportService");


// ==========================================================
// PDF REPORT SERVICE
// ==========================================================

class PdfReportService {


    // ======================================================
    // FORMAT TANGGAL
    // ======================================================

    formatDate(value) {

        if (!value) {

            return "";

        }

        const date =
            new Date(value);

        if (

            Number.isNaN(

                date.getTime()

            )

        ) {

            return value;

        }

        return date.toLocaleDateString(

            "id-ID",

            {

                day: "2-digit",

                month: "long",

                year: "numeric"

            }

        );

    }


    // ======================================================
    // GENERATE PDF
    // ======================================================

    generateReport(

        tanggalMulai,

        tanggalAkhir,

        outputPath

    ) {


        const branding =

            brandingService.getBranding();


        const summary =

            reportService.getSummary(

                tanggalMulai,

                tanggalAkhir

            );


        const outputDirectory =

            path.dirname(

                outputPath

            );


        if (

            !fs.existsSync(

                outputDirectory

            )

        ) {

            fs.mkdirSync(

                outputDirectory,

                {

                    recursive: true

                }

            );

        }


        const doc =

            new PDFDocument({

                size: "A4",

                margin: 50

            });


        const stream =

            fs.createWriteStream(

                outputPath

            );


        doc.pipe(stream);


        // ==============================================
        // HEADER
        // ==============================================

        this.drawHeader(

            doc,

            branding

        );


        // ==============================================
        // JUDUL
        // ==============================================

        doc.moveDown(2);


        doc

            .fontSize(16)

            .font("Helvetica-Bold")

            .text(

                "LAPORAN LAYANAN DIGITAL",

                {

                    align: "center"

                }

            );


        doc.moveDown(0.5);


        doc

            .fontSize(10)

            .font("Helvetica")

            .text(

                `Periode: ${this.formatDate(

                    tanggalMulai

                )} s.d. ${this.formatDate(

                    tanggalAkhir

                )}`,

                {

                    align: "center"

                }

            );


        doc.moveDown(2);


        // ==============================================
        // RINGKASAN ADMINISTRASI
        // ==============================================

        this.drawSectionTitle(

            doc,

            "A. PENGGUNAAN LAYANAN ADMINISTRASI"

        );


        this.drawRow(

            doc,

            "Pengguna Unik",

            summary

                .aktivitas

                .totalPenggunaAdministrasi

        );


        this.drawRow(

            doc,

            "Total Sesi Layanan",

            summary

                .aktivitas

                .totalSesiAdministrasi

        );


        doc.moveDown(1.5);


        // ==============================================
        // RINGKASAN ADUAN
        // ==============================================

        this.drawSectionTitle(

            doc,

            "B. PENGADUAN MASYARAKAT"

        );


        this.drawRow(

            doc,

            "Total Aduan",

            summary

                .aduan

                .totalAduan

        );


        this.drawRow(

            doc,

            "Baru",

            summary

                .aduan

                .baru

        );


        this.drawRow(

            doc,

            "Diproses",

            summary

                .aduan

                .diproses

        );


        this.drawRow(

            doc,

            "Menunggu Informasi",

            summary

                .aduan

                .menungguInfo

        );


        this.drawRow(

            doc,

            "Selesai",

            summary

                .aduan

                .selesai

        );


        // ==============================================
        // FOOTER
        // ==============================================

        this.drawFooter(

            doc,

            branding

        );


        doc.end();


        return new Promise(

            (

                resolve,

                reject

            ) => {


                stream.on(

                    "finish",

                    () => {

                        resolve(

                            outputPath

                        );

                    }

                );


                stream.on(

                    "error",

                    reject

                );


            }

        );

    }


    // ======================================================
    // HEADER
    // ======================================================

    drawHeader(

        doc,

        branding

    ) {


        const logoPath =

            branding.logoPath;


        if (

            logoPath &&

            fs.existsSync(

                logoPath

            )

        ) {


            doc.image(

                logoPath,

                50,

                40,

                {

                    fit: [

                        80,

                        80

                    ],

                    align: "center"

                }

            );

        }


        doc

            .fontSize(13)

            .font("Helvetica-Bold")

            .text(

                branding.namaKabupaten,

                150,

                45,

                {

                    width: 395,

                    align: "center"

                }

            );


        doc

            .fontSize(14)

            .font("Helvetica-Bold")

            .text(

                branding.namaInstansi,

                {

                    width: 395,

                    align: "center"

                }

            );


        doc.moveDown(0.5);


        doc

            .fontSize(11)

            .font("Helvetica-Bold")

            .text(

                branding.namaAplikasi,

                {

                    align: "center"

                }

            );


        doc

            .fontSize(9)

            .font("Helvetica")

            .text(

                branding.subjudulAplikasi,

                {

                    align: "center"

                }

            );


        doc.moveDown(0.5);


        doc

            .fontSize(8)

            .text(

                branding.alamat,

                {

                    align: "center"

                }

            );


        doc.text(

            `Website: ${branding.website} | ` +

            `Telp: ${branding.telepon}`,

            {

                align: "center"

            }

        );


        doc.text(

            `Email: ${branding.email}`,

            {

                align: "center"

            }

        );


        doc.moveDown(1);


        doc

            .moveTo(

                50,

                155

            )

            .lineTo(

                545,

                155

            )

            .stroke();

    }


    // ======================================================
    // JUDUL SECTION
    // ======================================================

    drawSectionTitle(

        doc,

        title

    ) {


        doc

            .fontSize(11)

            .font("Helvetica-Bold")

            .text(

                title

            );


        doc.moveDown(0.5);

    }


    // ======================================================
    // BARIS DATA
    // ======================================================

    drawRow(

        doc,

        label,

        value

    ) {


        doc

            .fontSize(10)

            .font("Helvetica")

            .text(

                `${label}: ${value}`

            );

    }


    // ======================================================
    // FOOTER
    // ======================================================

    drawFooter(

        doc,

        branding

    ) {


        const bottom =

            doc.page.height -

            70;


        doc

            .moveTo(

                50,

                bottom

            )

            .lineTo(

                545,

                bottom

            )

            .stroke();


        doc

            .fontSize(8)

            .font("Helvetica")

            .text(

                `Dokumen ini dibuat oleh ${

                    branding.namaAplikasi

                }`,

                50,

                bottom + 10,

                {

                    align: "center",

                    width: 495

                }

            );


        doc.text(

            `Dicetak: ${this.formatDate(

                new Date()

            )}`,

            {

                align: "center"

            }

        );

    }

}


// ==========================================================
// EXPORT
// ==========================================================

module.exports =

    new PdfReportService();