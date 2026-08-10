const XLSX = require("xlsx");
const path = require("path");

const FILE = path.join(
    __dirname,
    "../../backend/database/TERATAI_CORE.xlsx"
);

const SHEET = "AKTIVITAS";

const HEADERS = [

    "ID",
    "Waktu",
    "User_Key",
    "Identity_Type",
    "No_WA",
    "Nama",
    "Jenis_Aktivitas",
    "Kategori",
    "Referensi_ID"

];

class ActivityService {

    constructor() {

        this.reload();

    }

    reload() {

        this.workbook =
            XLSX.readFile(FILE);

        this.sheet =
            this.workbook.Sheets[SHEET];

        if (!this.sheet) {

            this.sheet =
                XLSX.utils.aoa_to_sheet([

                    HEADERS

                ]);

            XLSX.utils.book_append_sheet(

                this.workbook,

                this.sheet,

                SHEET

            );

            XLSX.writeFile(

                this.workbook,

                FILE

            );

        }

        this.records =
            XLSX.utils.sheet_to_json(

                this.sheet

            );

    }

    save() {

        this.workbook.Sheets[SHEET] =
            XLSX.utils.json_to_sheet(

                this.records,

                {

                    header: HEADERS

                }

            );

        XLSX.writeFile(

            this.workbook,

            FILE

        );

    }

    getCurrentDateTime() {

        const now =
            new Date();

        const formatter =
            new Intl.DateTimeFormat(

                "sv-SE",

                {

                    timeZone:
                        "Asia/Jakarta",

                    year:
                        "numeric",

                    month:
                        "2-digit",

                    day:
                        "2-digit",

                    hour:
                        "2-digit",

                    minute:
                        "2-digit",

                    second:
                        "2-digit",

                    hour12:
                        false

                }

            );

        const parts =
            formatter.formatToParts(

                now

            );

        const data = {};

        parts.forEach(

            part => {

                if (

                    part.type !==
                    "literal"

                ) {

                    data[part.type] =
                        part.value;

                }

            }

        );

        return `${data.year}-${data.month}-${data.day} ${data.hour}:${data.minute}:${data.second}`;

    }

    generateId() {

        const now =
            new Date();

        const tanggal =

            now.getFullYear() +

            String(

                now.getMonth() + 1

            ).padStart(

                2,

                "0"

            ) +

            String(

                now.getDate()

            ).padStart(

                2,

                "0"

            );

        const prefix =
            `ACT-${tanggal}-`;

        const today =
            this.records.filter(

                item =>

                    String(

                        item.ID || ""

                    ).startsWith(

                        prefix

                    )

            );

        return prefix +

            String(

                today.length + 1

            ).padStart(

                4,

                "0"

            );

    }

    record(data) {

        try {

            this.reload();

            this.records.push({

                ID:
                    this.generateId(),

                Waktu:
                    this.getCurrentDateTime(),

                User_Key:
                    data.User_Key || "",

                Identity_Type:
                    data.Identity_Type || "FALLBACK",

                No_WA:
                    data.No_WA || "",

                Nama:
                    data.Nama || "",

                Jenis_Aktivitas:
                    data.Jenis_Aktivitas || "",

                Kategori:
                    data.Kategori || "",

                Referensi_ID:
                    data.Referensi_ID || ""

            });

            this.save();

            return true;

        }

        catch (error) {

            console.error(

                "ACTIVITY SERVICE ERROR:",

                error

            );

            return false;

        }

    }

}

module.exports =
    new ActivityService();