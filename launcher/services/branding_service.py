"""
=====================================================
BRANDING SERVICE
=====================================================

Single Source Of Truth
untuk identitas, tema, dan konfigurasi aplikasi.

Semua window/module yang membutuhkan branding
WAJIB mengambil data melalui service ini.

Sumber konfigurasi:
    config/branding_config.json

Struktur:
    branding
    theme
    application
=====================================================
"""

import json
import os
from copy import deepcopy


class BrandingService:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        self.base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.config_path = os.path.join(
            self.base_dir,
            "config",
            "branding_config.json"
        )

        self.default_config = {
            "branding": {
                "system_name": "SATRIA MAS BINANGUN",
                "institution_name": "",
                "header_title": "",
                "header_description": "",
                "footer_text": "",
                "logo": "assets/logo.png"
            },

            "theme": {
                "mode": "light",
                "primary_color": "#12372A",
                "accent_color": "#2D6A4F",
                "background_color": "#F3F5F6",
                "card_color": "#FFFFFF",
                "text_color": "#12372A"
            },

            "application": {
                "version": "0.1.0",
                "environment": "production"
            }
        }

        self.config = {}

        self.load()

    # =====================================================
    # LOAD
    # =====================================================

    def load(self):

        if not os.path.exists(
            self.config_path
        ):

            print(
                "[BRANDING] Config belum ada. "
                "Membuat default."
            )

            self.config = deepcopy(
                self.default_config
            )

            self.save()

            return self.config

        try:

            with open(
                self.config_path,
                "r",
                encoding="utf-8"
            ) as file:

                loaded_config = json.load(file)

            self.config = self.normalize_config(
                loaded_config
            )

            return self.config

        except Exception as error:

            print(
                "[BRANDING ERROR] "
                "Gagal membaca config:",
                error
            )

            self.config = deepcopy(
                self.default_config
            )

            return self.config

    # =====================================================
    # NORMALIZE CONFIG
    # =====================================================

    def normalize_config(
        self,
        config
    ):

        if not isinstance(
            config,
            dict
        ):

            config = {}

        normalized = deepcopy(
            self.default_config
        )

        # =================================================
        # BRANDING
        # =================================================

        branding = config.get(
            "branding",
            {}
        )

        if isinstance(
            branding,
            dict
        ):

            normalized["branding"].update(
                branding
            )

        # =================================================
        # THEME
        # =================================================

        theme = config.get(
            "theme",
            {}
        )

        if isinstance(
            theme,
            dict
        ):

            normalized["theme"].update(
                theme
            )

        # =================================================
        # APPLICATION
        # =================================================

        application = config.get(
            "application",
            {}
        )

        if isinstance(
            application,
            dict
        ):

            normalized["application"].update(
                application
            )

        return normalized

    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        config=None
    ):

        if config is not None:

            self.config = self.normalize_config(
                config
            )

        folder = os.path.dirname(
            self.config_path
        )

        os.makedirs(
            folder,
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
    # RELOAD
    # =====================================================

    def reload(self):

        return self.load()

    # =====================================================
    # FULL CONFIG
    # =====================================================

    def get_config(self):

        return deepcopy(
            self.config
        )

    # =====================================================
    # BRANDING
    # =====================================================

    def get_branding(self):

        return deepcopy(
            self.config.get(
                "branding",
                {}
            )
        )

    # =====================================================
    # THEME
    # =====================================================

    def get_theme(self):

        return deepcopy(
            self.config.get(
                "theme",
                {}
            )
        )

    # =====================================================
    # APPLICATION
    # =====================================================

    def get_application(self):

        return deepcopy(
            self.config.get(
                "application",
                {}
            )
        )

    # =====================================================
    # GET VALUE
    # =====================================================

    def get(
        self,
        section,
        key,
        default=None
    ):

        return (
            self.config
            .get(
                section,
                {}
            )
            .get(
                key,
                default
            )
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
    # UPDATE APPLICATION
    # =====================================================

    def update_application(
        self,
        key,
        value
    ):

        if "application" not in self.config:

            self.config["application"] = {}

        self.config["application"][key] = value

        self.save()

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(self):

        required = [
            (
                "branding",
                "system_name"
            ),
            (
                "branding",
                "institution_name"
            )
        ]

        missing = []

        for section, key in required:

            value = (
                self.config
                .get(
                    section,
                    {}
                )
                .get(
                    key
                )
            )

            if not value:

                missing.append(
                    f"{section}.{key}"
                )

        return {
            "valid": len(missing) == 0,
            "missing": missing
        }

    # =====================================================
    # STATUS
    # =====================================================

    def get_status(self):

        validation = self.validate()

        return {
            "loaded": bool(
                self.config
            ),
            "valid": validation["valid"],
            "missing": validation["missing"],
            "path": self.config_path
        }


# =========================================================
# SINGLETON
# =========================================================

branding_service = BrandingService()