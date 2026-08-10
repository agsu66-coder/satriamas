const axios = require("axios");
const config = require("../config/config");

async function askAI(query) {

    try {

        const response = await axios.post(
            config.AI_ENDPOINT,
            {
                query
            },
            {
                timeout: 15000
            }
        );

        // Backend selalu mengembalikan object AIResponse
        return response.data;

    } catch (err) {

        console.error("[AI]", err.message);

        return {

            success: false,

            text: "Mohon maaf, mesin AI sedang tidak dapat dihubungi.",

            category: "",

            method: "error",

            confidence: 0

        };

    }

}

module.exports = {

    askAI

};