const { Client, LocalAuth } = require("whatsapp-web.js");

const client = new Client({
    authStrategy: new LocalAuth(),
});

client.on("ready", async () => {
    console.log("READY");

    try {
        const contact = await client.getContactById("6282227026480@c.us");
        console.log(contact);

        await client.sendMessage(
            "6282227026480@c.us",
            "Tes dari script sederhana"
        );

        console.log("BERHASIL");
    } catch (e) {
        console.error(e);
    }
});

client.initialize();