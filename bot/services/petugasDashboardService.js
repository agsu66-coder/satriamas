const aduanService =
    require("./aduanService");

const STATUS = {

    BARU: "BARU",

    DIPROSES: "DIPROSES",

    MENUNGGU_INFO: "MENUNGGU_INFO",

    SELESAI: "SELESAI"

};


class PetugasDashboardService {


    // =====================================
    // Semua aduan milik petugas
    // =====================================

    getMyComplaints(ownerId) {

        if (!ownerId) {

            return [];

        }

        return aduanService
            .getAll()
            .filter(

                aduan =>
                    aduan.Owner === ownerId

            );

    }


    // =====================================
    // Aduan berdasarkan status
    // =====================================

    getByStatus(ownerId, status) {

        return this
            .getMyComplaints(ownerId)
            .filter(

                aduan =>
                    aduan.Status === status

            );

    }


    // =====================================
    // Ringkasan dashboard
    // =====================================

    getSummary(ownerId) {

        const complaints =
            this.getMyComplaints(ownerId);

        return {

            total: complaints.length,

            baru:
                complaints.filter(

                    item =>
                        item.Status === STATUS.BARU

                ).length,

            diproses:
                complaints.filter(

                    item =>
                        item.Status === STATUS.DIPROSES

                ).length,

            menungguInfo:
                complaints.filter(

                    item =>
                        item.Status === STATUS.MENUNGGU_INFO

                ).length,

            selesai:
                complaints.filter(

                    item =>
                        item.Status === STATUS.SELESAI

                ).length

        };

    }


    // =====================================
    // Aduan terbaru
    // =====================================

    getLatest(ownerId, limit = 5) {

        return this
            .getMyComplaints(ownerId)
            .sort(

                (a, b) => {

                    const tanggalA =
                        new Date(
                            a.Tanggal_Update
                            || a.Tanggal
                        );

                    const tanggalB =
                        new Date(
                            b.Tanggal_Update
                            || b.Tanggal
                        );

                    return tanggalB - tanggalA;

                }

            )
            .slice(0, limit);

    }


    // =====================================
    // Statistik berdasarkan kategori
    // =====================================

    getCategorySummary(ownerId) {

        const complaints =
            this.getMyComplaints(ownerId);

        const result = {};

        complaints.forEach(

            aduan => {

                const kategori =
                    aduan.Kategori_ID
                    || "TANPA_KATEGORI";

                if (!result[kategori]) {

                    result[kategori] = 0;

                }

                result[kategori]++;

            }

        );

        return result;

    }

}


module.exports =
    new PetugasDashboardService();