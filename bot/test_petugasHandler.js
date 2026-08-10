const petugasHandler = require("./handlers/petugasHandler");
const conversationService = require("./services/conversationService");

conversationService.set("628123456789", {

    mode: "FEEDBACK",

    aduanId: "ADU-20260714-0004"

});

const msg = {

    from: "628123456789@c.us",

    body: "Perbaikan telah dilakukan.",

    reply: async (text) => {

        console.log("BOT:");
        console.log(text);

    }

};

petugasHandler.handlePetugas(null, msg);