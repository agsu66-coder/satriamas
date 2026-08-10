// ==========================================================
// KONFIGURASI
// ==========================================================

const BASE_URL =
    "http://127.0.0.1:5000";


// ==========================================================
// DATA UJI
// ==========================================================

const dataUji = {

    key:
        "ADUAN_FEEDBACK",

    data: {

        aduan_id:
            "ADU-20260722-TEST",

        feedback:
            "Aduan telah ditindaklanjuti oleh petugas."

    }

};


// ==========================================================
// HEADER
// ==========================================================

console.log("\n");

console.log(
    "=========================================================="
);

console.log(
    "🧪 TEST TEMPLATE ADUAN_FEEDBACK"
);

console.log(
    "=========================================================="
);

console.log("\n");


// ==========================================================
// TEST RENDER TEMPLATE
// ==========================================================

async function testRenderTemplate() {

    try {

        console.log(
            "📤 Mengirim permintaan render template..."
        );


        const response = await fetch(

            `${BASE_URL}/template/render`,

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body:
                    JSON.stringify(dataUji)

            }

        );


        const result =
            await response.json();


        console.log(
            "📥 Response Backend:"
        );

        console.log(result);


        if (!result.success) {

            throw new Error(

                "Backend mengembalikan success=false."

            );

        }


        if (!result.message) {

            throw new Error(

                "Pesan template kosong."

            );

        }


        console.log(

            "✅ LULUS: Template berhasil di-render."

        );


        if (

            !result.message.includes(

                dataUji.data.aduan_id

            )

        ) {

            throw new Error(

                "Placeholder {aduan_id} tidak berhasil diganti."

            );

        }


        console.log(

            "✅ LULUS: Placeholder {aduan_id} berhasil diganti."

        );


        if (

            !result.message.includes(

                dataUji.data.feedback

            )

        ) {

            throw new Error(

                "Placeholder {feedback} tidak berhasil diganti."

            );

        }


        console.log(

            "✅ LULUS: Placeholder {feedback} berhasil diganti."

        );


        console.log("\n");

        console.log(

            "📨 HASIL PESAN FINAL:"

        );

        console.log(

            "----------------------------------------------------------"

        );

        console.log(

            result.message

        );

        console.log(

            "----------------------------------------------------------"

        );


        console.log("\n");

        console.log(

            "🎉 TEST TEMPLATE ADUAN_FEEDBACK BERHASIL"

        );


    }

    catch (err) {

        console.error("\n");

        console.error(

            "❌ TEST GAGAL"

        );

        console.error(

            err.message

        );

        console.error("\n");

        process.exit(1);

    }

}


testRenderTemplate();