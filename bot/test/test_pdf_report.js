const path = require("path");

const pdfReportService =
    require(

        "../services/pdfReportService"

    );


console.log(

    "\n========================================"

);

console.log(

    "        TEST PDF REPORT SERVICE"

);

console.log(

    "========================================\n"

);


const outputPath =

    path.join(

        __dirname,

        "hasil_laporan_teratai.pdf"

    );


pdfReportService

    .generateReport(

        "2026-07-01",

        "2026-07-31",

        outputPath

    )

    .then(

        filePath => {


            console.log(

                "PDF BERHASIL DIBUAT"

            );


            console.log(

                "LOKASI FILE:"

            );


            console.log(

                filePath

            );


            console.log(

                "\n========================================"

            );


            console.log(

                "TEST PDF SELESAI"

            );


            console.log(

                "========================================\n"

            );

        }

    )

    .catch(

        error => {


            console.error(

                "\nERROR MEMBUAT PDF:"

            );


            console.error(

                error

            );

        }

    );