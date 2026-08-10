const dashboardService =
    require("../../bot/services/petugasDashboardService");

console.log(
    "===== DASHBOARD TEST ====="
);

const ownerId = "PTG001";

console.log(
    "OWNER :",
    ownerId
);

console.log(
    "\n=== SEMUA ADUAN ==="
);

console.log(

    dashboardService
        .getMyComplaints(ownerId)

);

console.log(
    "\n=== RINGKASAN ==="
);

console.log(

    dashboardService
        .getSummary(ownerId)

);

console.log(
    "\n=== ADUAN BARU ==="
);

console.log(

    dashboardService
        .getByStatus(

            ownerId,

            "BARU"

        )

);

console.log(
    "\n=== DIPROSES ==="
);

console.log(

    dashboardService
        .getByStatus(

            ownerId,

            "DIPROSES"

        )

);

console.log(
    "\n=== MENUNGGU INFO ==="
);

console.log(

    dashboardService
        .getByStatus(

            ownerId,

            "MENUNGGU_INFO"

        )

);

console.log(
    "\n=== SELESAI ==="
);

console.log(

    dashboardService
        .getByStatus(

            ownerId,

            "SELESAI"

        )

);