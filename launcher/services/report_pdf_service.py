import os

from datetime import datetime

from reportlab.lib import colors

from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT
)

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.units import cm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from services.branding_service import branding_service


class ReportPDFService:

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.title_style = self.styles["Heading1"]

        self.title_style.alignment = TA_CENTER

        self.heading_style = self.styles["Heading2"]

        self.heading_style.alignment = TA_LEFT

        self.normal_style = self.styles["BodyText"]


    # =====================================================
    # BRANDING
    # =====================================================

    def get_branding_data(self):

        branding = (
            branding_service
            .get_branding()
        )

        theme = (
            branding_service
            .get_theme()
        )

        application = (
            branding_service
            .get_application()
        )

        return {
            "branding": branding,
            "theme": theme,
            "application": application
        }


    # =====================================================
    # COLOR HELPER
    # =====================================================

    def get_color(
        self,
        value,
        fallback
    ):

        try:

            return colors.HexColor(
                value or fallback
            )

        except Exception:

            return colors.HexColor(
                fallback
            )


    # =====================================================
    # GENERATE PDF
    # =====================================================

    def generate_pdf(
        self,
        summary,
        output_file
    ):

        # ==================================================
        # VALIDATION
        # ==================================================

        if not summary:

            raise ValueError(
                "Data laporan kosong."
            )


        # ==================================================
        # OUTPUT DIRECTORY
        # ==================================================

        folder = os.path.dirname(
            output_file
        )

        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )


        # ==================================================
        # BRANDING
        # ==================================================

        branding_data = (
            self.get_branding_data()
        )

        branding = (
            branding_data["branding"]
        )

        theme = (
            branding_data["theme"]
        )

        application = (
            branding_data["application"]
        )


        # ==================================================
        # IDENTITY
        # ==================================================

        system_name = branding.get(
            "system_name",
            "SATRIA MAS BINANGUN"
        )

        institution_name = branding.get(
            "institution_name",
            ""
        )

        header_title = branding.get(
            "header_title",
            ""
        )

        header_description = branding.get(
            "header_description",
            ""
        )

        footer_text = branding.get(
            "footer_text",
            ""
        )

        logo_path = branding.get(
            "logo",
            ""
        )


        # ==================================================
        # APPLICATION
        # ==================================================

        application_version = application.get(
            "version",
            ""
        )

        application_environment = application.get(
            "environment",
            ""
        )


        # ==================================================
        # THEME
        # ==================================================

        primary_color = self.get_color(
            theme.get(
                "primary_color"
            ),
            "#12372A"
        )

        accent_color = self.get_color(
            theme.get(
                "accent_color"
            ),
            "#2D6A4F"
        )

        text_color = self.get_color(
            theme.get(
                "text_color"
            ),
            "#12372A"
        )

        muted_color = colors.HexColor(
            "#64748B"
        )

        border_color = colors.HexColor(
            "#CBD5E1"
        )

        white_color = colors.white


        # ==================================================
        # DOCUMENT
        # ==================================================

        document = SimpleDocTemplate(

            output_file,

            pagesize=A4,

            leftMargin=1.8 * cm,

            rightMargin=1.8 * cm,

            topMargin=1.8 * cm,

            bottomMargin=1.8 * cm

        )


        story = []


        # ==================================================
        # HEADER
        # ==================================================

        if (

            logo_path

            and

            os.path.exists(
                logo_path
            )

        ):

            try:

                logo = Image(

                    logo_path,

                    width=2.5 * cm,

                    height=2.5 * cm

                )

                logo.hAlign = "CENTER"

                story.append(
                    logo
                )

                story.append(
                    Spacer(
                        1,
                        0.25 * cm
                    )
                )

            except Exception as error:

                print(
                    "[REPORT PDF] "
                    "Logo gagal dimuat:",
                    error
                )


        # ==================================================
        # SYSTEM NAME
        # ==================================================

        story.append(

            Paragraph(

                system_name,

                self.title_style

            )

        )


        # ==================================================
        # INSTITUTION
        # ==================================================

        if institution_name:

            story.append(

                Paragraph(

                    institution_name,

                    self.heading_style

                )

            )


        # ==================================================
        # HEADER TITLE
        # ==================================================

        if header_title:

            story.append(

                Paragraph(

                    header_title,

                    self.normal_style

                )

            )


        # ==================================================
        # HEADER DESCRIPTION
        # ==================================================

        if header_description:

            story.append(

                Paragraph(

                    header_description,

                    self.normal_style

                )

            )


        story.append(

            Spacer(

                1,

                0.4 * cm

            )

        )


        # ==================================================
        # REPORT TITLE
        # ==================================================

        story.append(

            Paragraph(

                "<b>LAPORAN AKTIVITAS SISTEM</b>",

                self.heading_style

            )

        )


        story.append(

            Spacer(

                1,

                0.3 * cm

            )

        )


        # ==================================================
        # RINGKASAN AKTIVITAS
        # ==================================================

        story.append(

            Paragraph(

                "<b>RINGKASAN AKTIVITAS</b>",

                self.heading_style

            )

        )


        story.append(

            Spacer(

                1,

                0.25 * cm

            )

        )


        aktivitas = summary.get(
            "aktivitas",
            {}
        )

        periode = summary.get(
            "periode",
            {}
        )


        activity_table = [

            [
                "Informasi",
                "Nilai"
            ],

            [
                "Total Aktivitas",
                aktivitas.get(
                    "totalAktivitas",
                    0
                )
            ],

            [
                "Pengguna Unik",
                aktivitas.get(
                    "totalPenggunaUnik",
                    0
                )
            ],

            [
                "Pengguna Administrasi",
                aktivitas.get(
                    "totalPenggunaAdministrasi",
                    0
                )
            ],

            [
                "Total Sesi Administrasi",
                aktivitas.get(
                    "totalSesiAdministrasi",
                    0
                )
            ]

        ]


        table = Table(

            activity_table,

            colWidths=[

                11 * cm,

                4 * cm

            ]

        )


        table.setStyle(

            self.create_table_style(
                primary_color
            )

        )


        story.append(
            table
        )


        story.append(

            Spacer(

                1,

                0.6 * cm

            )

        )


        # ==================================================
        # AKTIVITAS BERDASARKAN JENIS
        # ==================================================

        story.append(

            Paragraph(

                "<b>AKTIVITAS BERDASARKAN JENIS</b>",

                self.heading_style

            )

        )


        story.append(

            Spacer(

                1,

                0.25 * cm

            )

        )


        aktivitas_per_jenis = aktivitas.get(

            "aktivitasPerJenis",

            {}

        )


        jenis_table = [

            [
                "Jenis Aktivitas",
                "Jumlah"
            ]

        ]


        for jenis, jumlah in (
            aktivitas_per_jenis.items()
        ):

            jenis_table.append(

                [
                    jenis,
                    jumlah
                ]

            )


        table = Table(

            jenis_table,

            colWidths=[

                11 * cm,

                4 * cm

            ]

        )


        table.setStyle(

            self.create_table_style(
                accent_color
            )

        )


        story.append(
            table
        )


        story.append(

            Spacer(

                1,

                0.6 * cm

            )

        )


        # ==================================================
        # INFORMASI LAPORAN
        # ==================================================

        story.append(

            Paragraph(

                "<b>INFORMASI LAPORAN</b>",

                self.heading_style

            )

        )


        story.append(

            Spacer(

                1,

                0.25 * cm

            )

        )


        periode_mulai = periode.get(
            "mulai",
            "-"
        )

        periode_akhir = periode.get(
            "akhir",
            "-"
        )


        version_text = (

            application_version

            if application_version

            else "-"

        )


        environment_text = (

            application_environment

            if application_environment

            else "-"

        )


        metadata_table = [

            [
                "Informasi",
                "Nilai"
            ],

            [
                "Periode",
                f"{periode_mulai} s/d "
                f"{periode_akhir}"
            ],

            [
                "Tanggal Cetak",
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            ],

            [
                "Versi Aplikasi",
                version_text
            ],

            [
                "Environment",
                environment_text
            ]

        ]


        table = Table(

            metadata_table,

            colWidths=[

                6 * cm,

                9 * cm

            ]

        )


        table.setStyle(

            self.create_table_style(
                primary_color
            )

        )


        story.append(
            table
        )


        story.append(

            Spacer(

                1,

                0.8 * cm

            )

        )


        # ==================================================
        # RINGKASAN ADUAN
        # ==================================================

        story.append(

            Paragraph(

                "<b>RINGKASAN ADUAN</b>",

                self.heading_style

            )

        )


        story.append(

            Spacer(

                1,

                0.25 * cm

            )

        )


        aduan = summary.get(
            "aduan",
            {}
        )


        complaint_table = [

            [
                "Informasi",
                "Nilai"
            ],

            [
                "Total Aduan",
                aduan.get(
                    "totalAduan",
                    0
                )
            ],

            [
                "Pengguna Aduan",
                aduan.get(
                    "totalPenggunaAduan",
                    0
                )
            ],

            [
                "Baru",
                aduan.get(
                    "baru",
                    0
                )
            ],

            [
                "Diproses",
                aduan.get(
                    "diproses",
                    0
                )
            ],

            [
                "Menunggu Info",
                aduan.get(
                    "menungguInfo",
                    0
                )
            ],

            [
                "Selesai",
                aduan.get(
                    "selesai",
                    0
                )
            ]

        ]


        table = Table(

            complaint_table,

            colWidths=[

                11 * cm,

                4 * cm

            ]

        )


        table.setStyle(

            self.create_table_style(
                accent_color
            )

        )


        story.append(
            table
        )


        story.append(

            Spacer(

                1,

                0.6 * cm

            )

        )


        # ==================================================
        # REKAP ADUAN PER PETUGAS
        # ==================================================

        story.append(

            Paragraph(

                "<b>REKAP ADUAN PER PETUGAS</b>",

                self.heading_style

            )

        )


        story.append(

            Spacer(

                1,

                0.25 * cm

            )

        )


        petugas = aduan.get(

            "aduanPerPetugas",

            {}

        )


        petugas_table = [

            [
                "Petugas",
                "Jumlah Aduan"
            ]

        ]


        if petugas:

            for nama, jumlah in (
                petugas.items()
            ):

                if nama == "-":

                    nama = "Belum Ditugaskan"


                petugas_table.append(

                    [
                        nama,
                        jumlah
                    ]

                )

        else:

            petugas_table.append(

                [
                    "Belum Ditugaskan",
                    0
                ]

            )


        table = Table(

            petugas_table,

            colWidths=[

                11 * cm,

                4 * cm

            ]

        )


        table.setStyle(

            self.create_table_style(
                accent_color
            )

        )


        story.append(
            table
        )


        story.append(

            Spacer(

                1,

                0.8 * cm

            )

        )


        # ==================================================
        # FOOTER
        # ==================================================

        footer_display = (

            footer_text

            if footer_text

            else (

                f"{institution_name} • "
                f"{datetime.now().year}"

            )

        )


        footer_table = Table(

            [

                [

                    footer_display,

                    datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )

                ],

                [

                    "Laporan dihasilkan "
                    "secara otomatis.",

                    system_name

                ]

            ],

            colWidths=[

                9 * cm,

                6 * cm

            ]

        )


        footer_table.setStyle(

            TableStyle([

                (

                    "LINEABOVE",

                    (0, 0),

                    (-1, 0),

                    0.6,

                    border_color

                ),

                (

                    "TEXTCOLOR",

                    (0, 0),

                    (-1, -1),

                    muted_color

                ),

                (

                    "FONTNAME",

                    (0, 0),

                    (-1, -1),

                    "Helvetica"

                ),

                (

                    "FONTSIZE",

                    (0, 0),

                    (-1, -1),

                    8

                ),

                (

                    "ALIGN",

                    (1, 0),

                    (1, -1),

                    "RIGHT"

                ),

                (

                    "TOPPADDING",

                    (0, 0),

                    (-1, -1),

                    6

                )

            ])

        )


        story.append(
            footer_table
        )


        # ==================================================
        # BUILD PDF
        # ==================================================

        document.build(
            story
        )


        return output_file


    # =====================================================
    # TABLE STYLE
    # =====================================================

    def create_table_style(
        self,
        header_color
    ):

        return TableStyle([

            (

                "GRID",

                (0, 0),

                (-1, -1),

                0.4,

                colors.grey

            ),

            (

                "BACKGROUND",

                (0, 0),

                (-1, 0),

                header_color

            ),

            (

                "TEXTCOLOR",

                (0, 0),

                (-1, 0),

                colors.white

            ),

            (

                "FONTNAME",

                (0, 0),

                (-1, 0),

                "Helvetica-Bold"

            ),

            (

                "FONTNAME",

                (0, 1),

                (0, -1),

                "Helvetica-Bold"

            ),

            (

                "ALIGN",

                (1, 1),

                (1, -1),

                "CENTER"

            ),

            (

                "BOTTOMPADDING",

                (0, 0),

                (-1, -1),

                6

            ),

            (

                "TOPPADDING",

                (0, 0),

                (-1, -1),

                6

            )

        ])


# =========================================================
# SINGLETON
# =========================================================

report_pdf_service = ReportPDFService()