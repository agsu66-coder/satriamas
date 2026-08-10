const aduanService =
require("./services/aduanService");

console.log(
    "SEMUA ADUAN :",
    aduanService.getAll()
);

console.log(
    "ADUAN PTG001 :",
    aduanService.getByOwner("PTG001")
);

console.log(
    "ADUAN BARU PTG001 :",
    aduanService.getByOwnerAndStatus(
        "PTG001",
        "BARU"
    )
);

console.log(
    "ADUAN MENUNGGU INFO PTG001 :",
    aduanService.getByOwnerAndStatus(
        "PTG001",
        "MENUNGGU_INFO"
    )
);