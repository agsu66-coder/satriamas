const stateService =
    require("../services/stateService");

const aiClient =
    require("../services/aiClient");

// simulasi nomor WA

const USER =
    "628123456789";


async function simulate(message){


    console.log("\n====================");
    console.log("USER:");
    console.log(message);


    const session =
        stateService.getState(USER);



    // MENU ADMIN

    if(message === "1"){

        stateService.setState(
            USER,
            {
                state:"ADMIN"
            }
        );


        console.log(
            "BOT: Silakan tuliskan pertanyaan administrasi Anda."
        );

        return;

    }



    // ADMIN

    if(
        session?.state === "ADMIN" ||
        session?.state === "ADMIN_ACTIVE"
    ){


        const response =
            await aiClient.askAI(
                message
            );


        console.log(
            "BOT:",
            response.text
        );


        stateService.setState(
            USER,
            {
                state:"ADMIN_ACTIVE"
            }
        );


        console.log(
            "STATE:",
            stateService.getState(USER)
        );


        return;

    }


    console.log(
        "BOT: Pilih menu dahulu"
    );

}



async function run(){


    await simulate("1");


    await simulate(
        "Saya ingin membuat KK baru"
    );


    await simulate(
        "KTP saya hilang"
    );


    await simulate(
        "berapa harga motor bekas"
    );


}


run();