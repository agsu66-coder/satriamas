const BACKEND_URL =
    "http://127.0.0.1:5000";


// ==========================================================
// RENDER TEMPLATE DARI BACKEND
// ==========================================================

async function renderTemplate(key, data = {}) {

    const response = await fetch(

        `${BACKEND_URL}/template/render`,

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"

            },

            body: JSON.stringify({

                key,

                data

            })

        }

    );


    const result =
        await response.json();


    if (!response.ok || !result.success) {

        throw new Error(

            result.message
            ||
            "Gagal mengambil template dari backend."

        );

    }


    return result.message;

}


module.exports = {

    renderTemplate

};