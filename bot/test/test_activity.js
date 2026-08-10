const activityService =
    require("../services/activityService");

console.log(
    "\n===== TEST ACTIVITY SERVICE =====\n"
);

const result =
    activityService.record({

        User_Key:
            "628123456789",

        Identity_Type:
            "PHONE",

        No_WA:
            "628123456789",

        Nama:
            "TEST USER",

        Jenis_Aktivitas:
            "AKSES_LAYANAN",

        Kategori:
            "ADMINISTRASI",

        Referensi_ID:
            ""

    });

console.log(
    "HASIL RECORD:",
    result
);

console.log(
    "\n===== TEST SELESAI =====\n"
);