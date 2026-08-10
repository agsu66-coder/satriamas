const reportService =
    require("../services/reportService");

console.log(
    "\n===== TEST REPORT SERVICE =====\n"
);

const result =
    reportService.getSummary(

        "2026-07-01",

        "2026-07-31"

    );

console.log(

    JSON.stringify(

        result,

        null,

        4

    )

);

console.log(
    "\n===== TEST SELESAI =====\n"
);