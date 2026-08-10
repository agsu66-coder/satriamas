import json
import os


class BrandingService:

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        self.base_dir = os.path.dirname(

            os.path.dirname(

                os.path.abspath(

                    __file__

                )

            )

        )

        self.config_path = os.path.join(

            self.base_dir,

            "config",

            "branding_config.json"

        )

        self.default_config = {

            "branding": {

                "system_name":

                    "SATRIA MAS",

                "institution_name":

                    "Kecamatan Binangun",

                "header_title":

                    "Asisten Digital Kecamatan Binangun",

                "header_description":

                    (

                        "Sarana Informasi Terpadu "

                        "dan Aduan Masyarakat "

                        "Kecamatan Binangun"

                    ),

                "footer_text":

                    "© 2026 Kecamatan Binangun",

                "logo":

                    "assets/logo.png"

            },

            "theme": {

                "mode":

                    "dark",

                "primary_color":

                    "#12372A",

                "accent_color":

                    "#2D6A4F"

            }

        }

        self.config = self.load()


    # =====================================================
    # LOAD CONFIG
    # =====================================================

    def load(self):

        if not os.path.exists(

            self.config_path

        ):

            self.save(

                self.default_config

            )

            return self.default_config

        try:

            with open(

                self.config_path,

                "r",

                encoding="utf-8"

            ) as file:

                config = json.load(

                    file

                )

            return config

        except Exception as error:

            print(

                "Gagal membaca branding config:",

                error

            )

            return self.default_config


    # =====================================================
    # SAVE CONFIG
    # =====================================================

    def save(

        self,

        config=None

    ):

        if config is not None:

            self.config = config

        os.makedirs(

            os.path.dirname(

                self.config_path

            ),

            exist_ok=True

        )

        with open(

            self.config_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.config,

                file,

                indent=4,

                ensure_ascii=False

            )


    # =====================================================
    # GET BRANDING
    # =====================================================

    def get_branding(self):

        return self.config.get(

            "branding",

            {}

        )


    # =====================================================
    # GET THEME
    # =====================================================

    def get_theme(self):

        return self.config.get(

            "theme",

            {}

        )


    # =====================================================
    # UPDATE BRANDING
    # =====================================================

    def update_branding(

        self,

        key,

        value

    ):

        if "branding" not in self.config:

            self.config["branding"] = {}

        self.config["branding"][key] = value

        self.save()


    # =====================================================
    # UPDATE THEME
    # =====================================================

    def update_theme(

        self,

        key,

        value

    ):

        if "theme" not in self.config:

            self.config["theme"] = {}

        self.config["theme"][key] = value

        self.save()


    # =====================================================
    # RELOAD CONFIG
    # =====================================================

    def reload(self):

        self.config = self.load()

        return self.config


# =========================================================
# SINGLETON
# =========================================================

branding_service = BrandingService()