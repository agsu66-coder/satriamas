import os

import tkinter as tk

from tkinter import ttk

from tkinter import messagebox

from datetime import datetime

from tkcalendar import DateEntry

from tkinter import filedialog


from services.report_service import report_service

from services.report_pdf_service import report_pdf_service

from services.branding_service import branding_service


class ReportWindow:

    # ==================================================
    # INIT
    # ==================================================

    def __init__(

        self,

        parent,

        branding=None,

        current_user=None

    ):

        self.parent = parent

        self.current_user = current_user

        self.report_summary = None

        # ==================================================
        # BRANDING SINGLE SOURCE OF TRUTH
        # ==================================================

        self.branding = branding_service.get_branding()

        self.theme = branding_service.get_theme()

        self.application = branding_service.get_application()

        # ==================================================
        # IDENTITY
        # ==================================================

        self.system_name = self.branding.get(
            "system_name",
            "SATRIA MAS BINANGUN"
        )

        self.institution_name = self.branding.get(
            "institution_name",
            ""
        )

        self.header_title = self.branding.get(
            "header_title",
            ""
        )

        self.footer_text = self.branding.get(
            "footer_text",
            ""
        )

        # ==================================================
        # THEME
        # ==================================================

        self.primary_color = self.theme.get(
            "primary_color",
            "#12372A"
        )

        self.accent_color = self.theme.get(
            "accent_color",
            "#2D6A4F"
        )

        self.background_color = self.theme.get(
            "background_color",
            "#F3F5F6"
        )

        self.card_color = self.theme.get(
            "card_color",
            "#FFFFFF"
        )

        self.text_color = self.theme.get(
            "text_color",
            "#12372A"
        )

        self.muted_color = "#64748B"


        # ==================================================
        # WINDOW
        # ==================================================

        self.window = tk.Toplevel(

            self.parent

        )


        self.window.title(

            "LAPORAN - "

            + self.system_name

        )


        self.window.geometry(

            "950x700"

        )


        self.window.minsize(

            750,

            500

        )


        self.window.configure(

            bg=self.background_color

        )


        # ==================================================
        # BUILD
        # ==================================================

        self.build_ui()


    # ==================================================
    # BUILD UI
    # ==================================================

    def build_ui(self):

        # ==================================================
        # HEADER
        # ==================================================

        header = tk.Frame(

            self.window,

            bg=self.primary_color,

            height=90

        )


        header.pack(

            fill="x"

        )


        header.pack_propagate(

            False

        )


        tk.Label(

            header,

            text="📊  LAPORAN " + self.system_name,

            font=(

                "Arial",

                20,

                "bold"

            ),

            fg="white",

            bg=self.primary_color

        ).pack(

            anchor="w",

            padx=25,

            pady=(18, 0)

        )


        tk.Label(

            header,

            text="Ringkasan aktivitas sistem dan aduan masyarakat",

            font=(

                "Arial",

                9

            ),

            fg="#D1FAE5",

            bg=self.primary_color

        ).pack(

            anchor="w",

            padx=27

        )


        # ==================================================
        # MAIN CONTAINER
        # ==================================================

        main = tk.Frame(

            self.window,

            bg=self.background_color

        )


        main.pack(

            fill="both",

            expand=True

        )


        # ==================================================
        # CANVAS
        # ==================================================

        self.canvas = tk.Canvas(

            main,

            bg=self.background_color,

            highlightthickness=0

        )


        self.canvas.pack(

            side="left",

            fill="both",

            expand=True

        )


        # ==================================================
        # SCROLLBAR
        # ==================================================

        scrollbar = ttk.Scrollbar(

            main,

            orient="vertical",

            command=self.canvas.yview

        )


        scrollbar.pack(

            side="right",

            fill="y"

        )


        self.canvas.configure(

            yscrollcommand=scrollbar.set

        )


        # ==================================================
        # SCROLLABLE FRAME
        # ==================================================

        self.scrollable_frame = tk.Frame(

            self.canvas,

            bg=self.background_color

        )


        self.canvas_window = (

            self.canvas.create_window(

                (

                    0,

                    0

                ),

                window=self.scrollable_frame,

                anchor="nw"

            )

        )


        self.scrollable_frame.bind(

            "<Configure>",

            self.on_frame_configure

        )


        self.canvas.bind(

            "<Configure>",

            self.on_canvas_configure

        )


        self.canvas.bind(

            "<MouseWheel>",

            self.on_mousewheel

        )


        # ==================================================
        # FILTER SECTION
        # ==================================================

        self.build_filter_section()


        # ==================================================
        # SUMMARY SECTION
        # ==================================================

        self.build_summary_section()


        # ==================================================
        # FOOTER
        # ==================================================

        self.build_footer()


    # ==================================================
    # SCROLL CONFIGURATION
    # ==================================================

    def on_frame_configure(

        self,

        event=None

    ):

        self.canvas.configure(

            scrollregion=self.canvas.bbox(

                "all"

            )

        )


    def on_canvas_configure(

        self,

        event

    ):

        self.canvas.itemconfig(

            self.canvas_window,

            width=event.width

        )


    def on_mousewheel(

        self,

        event

    ):

        self.canvas.yview_scroll(

            int(

                -1 *

                (

                    event.delta

                    /

                    120

                )

            ),

            "units"

        )


    # ==================================================
    # FILTER SECTION
    # ==================================================

    def build_filter_section(self):

        section = tk.Frame(

            self.scrollable_frame,

            bg=self.background_color

        )


        section.pack(

            fill="x",

            padx=25,

            pady=25

        )


        tk.Label(

            section,

            text="PERIODE LAPORAN",

            font=(

                "Arial",

                16,

                "bold"

            ),

            fg=self.text_color,

            bg=self.background_color

        ).pack(

            anchor="w",

            pady=(0, 12)

        )


        filter_card = tk.Frame(

            section,

            bg=self.card_color,

            highlightbackground="#CBD5E1",

            highlightthickness=1

        )


        filter_card.pack(

            fill="x"

        )


        # ==================================================
        # FILTER CONTENT
        # ==================================================

        content = tk.Frame(

            filter_card,

            bg=self.card_color

        )


        content.pack(

            fill="x",

            padx=20,

            pady=20

        )


        # ==================================================
        # TANGGAL MULAI
        # ==================================================

        start_frame = tk.Frame(

            content,

            bg=self.card_color

        )


        start_frame.pack(

            side="left",

            padx=(0, 20)

        )


        tk.Label(

            start_frame,

            text="Tanggal Mulai",

            font=(

                "Arial",

                9,

                "bold"

            ),

            fg=self.text_color,

            bg=self.card_color

        ).pack(

            anchor="w"

        )


        self.start_date_entry = DateEntry(

            start_frame,

            width=18,

            date_pattern="yyyy-mm-dd",

            background=self.primary_color,

            foreground="white",

            borderwidth=2

        )


        self.start_date_entry.pack(

            pady=(5, 0)

        )


        # ==================================================
        # TANGGAL AKHIR
        # ==================================================

        end_frame = tk.Frame(

            content,

            bg=self.card_color

        )


        end_frame.pack(

            side="left",

            padx=(0, 20)

        )


        tk.Label(

            end_frame,

            text="Tanggal Akhir",

            font=(

                "Arial",

                9,

                "bold"

            ),

            fg=self.text_color,

            bg=self.card_color

        ).pack(

            anchor="w"

        )


        self.end_date_entry = DateEntry(

            end_frame,

            width=18,

            date_pattern="yyyy-mm-dd",

            background=self.primary_color,

            foreground="white",

            borderwidth=2

        )


        self.end_date_entry.pack(

            pady=(5, 0)

        )


        # ==================================================
        # BUTTON GENERATE
        # ==================================================

        tk.Button(

            content,

            text="🔍  TAMPILKAN LAPORAN",

            command=self.generate_report,

            font=(

                "Arial",

                10,

                "bold"

            ),

            fg="white",

            bg=self.accent_color,

            activebackground=self.primary_color,

            activeforeground="white",

            relief="flat",

            cursor="hand2",

            padx=15,

            pady=8

        ).pack(

            side="left",

            padx=10

        )


        # ==================================================
        # BUTTON PDF
        # ==================================================

        tk.Button(

            content,

            text="📄  EXPORT PDF",

            command=self.export_pdf,

            font=(

                "Arial",

                10,

                "bold"

            ),

            fg="white",

            bg="#607D8B",

            activebackground="#455A64",

            activeforeground="white",

            relief="flat",

            cursor="hand2",

            padx=15,

            pady=8

        ).pack(

            side="left"

        )


    # ==================================================
    # SUMMARY SECTION
    # ==================================================

    def build_summary_section(self):

        section = tk.Frame(

            self.scrollable_frame,

            bg=self.background_color

        )


        section.pack(

            fill="x",

            padx=25,

            pady=(0, 25)

        )


        tk.Label(

            section,

            text="RINGKASAN LAPORAN",

            font=(

                "Arial",

                16,

                "bold"

            ),

            fg=self.text_color,

            bg=self.background_color

        ).pack(

            anchor="w",

            pady=(0, 12)

        )


        self.preview_frame = tk.Frame(

            section,

            bg=self.background_color

        )


        self.preview_frame.pack(

            fill="both",

            expand=True


        )


    # ==================================================
    # FOOTER
    # ==================================================

    def build_footer(self):

        footer = tk.Frame(

            self.scrollable_frame,

            bg=self.background_color

        )


        footer.pack(

            fill="x",

            padx=25,

            pady=(0, 25)

        )

        branding = self.branding

        institution = branding.get(
                "institution_name",
                ""
        )

        tk.Label(

            footer,

            text=f"{institution} • {datetime.now().year}",

            font=(

                "Arial",

                9

            ),

            fg=self.muted_color,

            bg=self.background_color

        ).pack()


    # ==================================================
    # GET PERIOD
    # ==================================================

    def get_period(self):

        start_date = (

            self.start_date_entry

            .get_date()

        )


        end_date = (

            self.end_date_entry

            .get_date()

        )


        if start_date > end_date:

            messagebox.showerror(

                "Periode Tidak Valid",

                "Tanggal mulai tidak boleh lebih besar "

                "dari tanggal akhir."

            )

            return None, None


        return start_date, end_date


    # ==================================================
    # GENERATE REPORT
    # ==================================================

    def generate_report(self):

        try:

            start_date, end_date = (

                self.get_period()

            )


            if not start_date:

                return


            report_data = (

                report_service.get_summary(

                    start_date,

                    end_date

                )

            )

            self.report_summary = report_data

            self.display_report(

                report_data

            )


        except Exception as error:

            messagebox.showerror(

                "Gagal Memuat Laporan",

                str(error)

            )



    # ==================================================
    # DISPLAY REPORT
    # ==================================================

    def display_report(

        self,

        report_data

    ):


        self.report_summary = report_data


        for widget in self.preview_frame.winfo_children():

            widget.destroy()


        container = tk.Frame(

            self.preview_frame,

            bg=self.background_color

        )


        container.pack(

            fill="x"

        )



        aktivitas = report_data["aktivitas"]

        aduan = report_data["aduan"]



        cards = [

            (

                "Aktivitas",

                aktivitas["totalAktivitas"]

            ),

            (

                "Pengguna",

                aktivitas["totalPenggunaUnik"]

            ),

            (

                "Administrasi",

                aktivitas["totalSesiAdministrasi"]

            ),

            (

                "Aduan",

                aduan["totalAduan"]

            ),

            (

                "Selesai",

                aduan["selesai"]

            )

        ]



        for index, item in enumerate(cards):


            card = self.create_card(

                container,

                item[0],

                item[1]

            )


            card.grid(

                row=0,

                column=index,

                padx=8,

                sticky="nsew"

            )


            container.grid_columnconfigure(

                index,

                weight=1

            )

        # ==================================================
        # AKTIVITAS BERDASARKAN JENIS
        # ==================================================

        aktivitas_frame = tk.LabelFrame(

                self.preview_frame,

                text="AKTIVITAS BERDASARKAN JENIS",

                font=(

                        "Arial",

                        10,

                        "bold"

                ),

                bg=self.background_color,

                fg=self.text_color,

                padx=10,

                pady=10

        )


        aktivitas_frame.pack(

                fill="x",

                pady=(20,10)

        )


        aktivitas_per_jenis = report_data["aktivitas"].get(

                "aktivitasPerJenis",

                {}

        )


        for jenis, jumlah in aktivitas_per_jenis.items():

                row = tk.Frame(

                        aktivitas_frame,

                        bg=self.background_color

                )


                row.pack(

                        fill="x",

                        pady=2

                )


                tk.Label(

                        row,

                        text=jenis,

                        bg=self.background_color,

                        anchor="w"

                ).pack(

                        side="left"

                )


                tk.Label(

                        row,

                        text=str(jumlah),

                        bg=self.background_color,

                        font=(

                                "Arial",

                                10,

                                "bold"

                        )

                ).pack(

                        side="right"

                )

        # ==================================================
        # STATUS ADUAN
        # ==================================================

        aduan_frame = tk.LabelFrame(

                self.preview_frame,

                text="STATUS ADUAN",

                font=(

                        "Arial",

                        10,

                        "bold"

                ),

                bg=self.background_color,

                fg=self.text_color,

                padx=10,

                pady=10

        )


        aduan_frame.pack(

                fill="x",

                pady=(0,10)

        )


        aduan = report_data["aduan"]


        rows = [

                ("Baru", aduan["baru"]),

                ("Diproses", aduan["diproses"]),

                ("Menunggu Info", aduan["menungguInfo"]),

                ("Selesai", aduan["selesai"])

        ]


        for nama, nilai in rows:

                row = tk.Frame(

                        aduan_frame,

                        bg=self.background_color

                )


                row.pack(

                        fill="x",

                        pady=2

                )


                tk.Label(

                        row,

                        text=nama,

                        bg=self.background_color

                ).pack(

                        side="left"

                )


                tk.Label(

                        row,

                        text=str(nilai),

                        bg=self.background_color,

                        font=(

                                "Arial",

                                10,

                                "bold"

                        )

                ).pack(

                        side="right"

                )

        # ==================================================
        # ADUAN PER PETUGAS
        # ==================================================

        petugas_frame = tk.LabelFrame(

                self.preview_frame,

                text="ADUAN PER PETUGAS",

                font=(

                      "Arial",

                      10,

                      "bold"

                ),

                bg=self.background_color,

                fg=self.text_color,

                padx=10,

                pady=10
        )

        petugas_frame.pack(

                fill="x",


                pady=(0, 10)

        )


        aduan_petugas = aduan.get(

                "aduanPerPetugas",

                {}

        )


        for petugas, jumlah in aduan_petugas.items():

                if petugas == "-":

                        petugas = "Belum Ditugaskan"


                row = tk.Frame(

                        petugas_frame,

                        bg=self.background_color

                )


                row.pack(

                        fill="x",

                        pady=2

                )


                tk.Label(

                        row,

                        text=petugas,

                        bg=self.background_color

                ).pack(

                        side="left"

                )


                tk.Label(

                        row,

                        text=str(jumlah),

                        bg=self.background_color,

                        font=(

                                "Arial",

                                10,

                                "bold"

                        )

                ).pack(

                        side="right"

                )

    # ==================================================
    # CARD BUILDER
    # ==================================================

    def create_card(

        self,

        parent,

        title,

        value,

        color=None

    ):


        if color is None:

            color = self.primary_color



        frame = tk.Frame(

            parent,

            bg=self.card_color,

            bd=1,

            relief="solid"

        )



        tk.Label(

            frame,

            text=title,

            font=(

                "Arial",

                10,

                "bold"

            ),

            bg=self.card_color,

            fg=self.muted_color

        ).pack(

            pady=(12,5)

        )



        tk.Label(

            frame,

            text=str(value),

            font=(

                "Arial",

                22,

                "bold"

            ),

            bg=self.card_color,

            fg=color

        ).pack(

            pady=(0,12)

        )


        return frame

    # ==================================================
    # EXPORT PDF
    # ==================================================

    def export_pdf(self):

        try:

            start_date, end_date = (

                self.get_period()

            )


            if not start_date:

                return


            summary = (

                report_service.get_summary(

                    start_date,

                    end_date

                )

            )


            filename = filedialog.asksaveasfilename(

                title="Simpan Laporan PDF",

                defaultextension=".pdf",

                filetypes=[

                    (

                        "PDF File",

                        "*.pdf"

                    )

                ],

                initialfile=f"Laporan_{self.system_name}.pdf"

            )


            if not filename:

                return


            report_pdf_service.generate_pdf(

                summary,

                filename

            )


            messagebox.showinfo(

                self.system_name,

                "Laporan berhasil disimpan.\n\n"

                + filename

            )


            os.startfile(

                filename

            )


        except Exception as error:


            messagebox.showerror(

                self.system_name,

                str(error)

            )
    # ==================================================
    # RUN
    # ==================================================

    def run(self):

        self.window.grab_set()

        self.window.focus_force()