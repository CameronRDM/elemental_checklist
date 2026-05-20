import tkinter as tk
from tkinter import ttk
import json
import os

# ==========================================
# ELEMENTAL CREATURES CHECKLIST
# ==========================================

SAVE_FILE = "elemental_progress.json"

# ==========================================
# CREATURE LIST
# ==========================================

creatures = [
    ("001", "Montigo"),
    ("002", "Brukey"),
    ("003", "Felixir"),
    ("004", "Daereap"),
    ("005", "Naryu"),
    ("006", "Venwurm"),
    ("007", "Olivkron"),
    ("008", "Nimbken"),
    ("009", "Omnigon"),
    ("010", "Chowler"),
    ("011", "Zimble"),
    ("012", "Grizler"),
    ("013", "Calfarak"),
    ("014", "Mammo"),
    ("015", "Startle"),
    ("016", "Natuko"),
    ("017", "Torcos"),
    ("018", "Rhiyu"),
    ("019", "Pyrogon"),
    ("020", "Arrowkin"),
    ("021", "Verglamo"),
    ("022", "Tedge"),
    ("023", "Nagi"),
    ("024", "Gorock"),
    ("025", "Staratic"),
    ("026", "Akusa"),
    ("027", "Soulyote"),
    ("028", "Komori"),
    ("029", "Rox"),
    ("030", "Mahzi"),
    ("031", "Subursa"),
    ("032", "Wattpod"),
    ("033", "Aquazard"),
    ("034", "Torva"),
    ("035", "Sequoiadon"),
    ("036", "Noxvil"),
    ("037", "Lytviper"),
    ("038", "Fubair"),
    ("039", "Rocwyler"),
    ("040", "Monfire"),
    ("041", "Kairiel"),
    ("042", "Frorilla"),
    ("043", "Zahnyo"),
    ("044", "Fyerguar"),
    ("045", "Finnym"),
    ("046", "Zafar"),
    ("047", "Splicer"),
    ("048", "Rakoda"),
    ("049", "Daracarid"),
    ("050", "Darnimbus"),
    ("051", "Darcolgon"),
    ("052", "Gurukey"),
    ("053", "Armodon"),
    ("054", "Qwell"),
    ("055", "Elemor"),
    ("056", "Rosleo"),
    ("057", "Wolfree"),
    ("058", "Moakey"),
    ("059", "Zenoo"),
    ("060", "Phantsea"),
    ("061", "Elecrus"),
    ("062", "Galawolf"),
    ("063", "Cobreez"),
    ("064", "Boulbear"),
    ("065", "Bulfin"),
    ("066", "Heckle"),
    ("067", "Rashee"),
    ("068", "Zephyram"),
    ("069", "Prismeetle"),
    ("070", "Rygon"),
    ("071", "Rolem"),
    ("072", "Norgon"),
    ("073", "Vametric"),
    ("074", "Plaeger"),
    ("075", "Brawlake"),
    ("076", "Corezone"),
    ("077", "Thoryu"),
    ("078", "Norskyathan"),
    ("079", "Konmoncane"),
    ("080", "Steamlox"),
    ("081", "Rahgashok"),
    ("082", "Kenku"),
    ("083", "Darpendos"),
    ("084", "Psygorokong"),
    ("085", "Jagutrap"),
    ("086", "Thermoshin"),
    ("087", "Kodemtha"),
    ("088", "Caligmium"),
    ("089", "Arbouloo"),
    ("090", "Burudosh"),
    ("091", "Cykumo"),
    ("092", "Jinmitsu"),
    ("093", "Chaoseus"),
    ("094", "Scykenshin"),
    ("095", "Grizgroun"),
    ("096", "Boultorbine"),
    ("097", "Greywint"),
    ("098", "Maneferno"),
    ("099", "Qwirlyte"),
    ("100", "Almegra"),
    ("101", "Zodrus"),
    ("102", "Zunderga"),
    ("103", "Juntungo"),
    ("104", "Daekuma"),
    ("105", "Rygalagon"),
    ("106", "Mamchi"),
    ("107", "Nebu"),
    ("108", "Walanos"),
    ("109", "Typerionrex"),
    ("110", "Screereap"),
    ("111", "Depthadon"),
    ("112", "Wolruroot"),
    ("113", "Mounrongo"),
    ("114", "Plutanis"),
    ("115", "Zalimbo"),
    ("116", "Seawingo"),
    ("117", "Sharleopur"),
    ("118", "Coliamoth"),
    ("119", "Duskthorn"),
    ("120", "Volgairo"),
    ("121", "Darayabolt"),
    ("122", "Darakmador"),
    ("123", "Darcalient"),
    ("124", "Shinmanari"),
    ("125", "Wenyido"),
    ("126", "Burburnape"),
    ("127", "Phanto"),
    ("128", "Concoradu"),
    ("129", "Zuritia"),
    ("130", "Granghoul"),
    ("131", "Rivairmo"),
    ("132", "Catlumax"),
    ("133", "Fuegofloradon"),
    ("134", "Rebbleram"),
    ("135", "Bonegar"),
    ("136", "Snowlurger"),
    ("137", "Kilmbair"),
    ("138", "Vortauro"),
    ("139", "Seerzoose"),
    ("140", "Zorrok"),
    ("141", "Frigidnix"),
    ("142", "Vermburro"),
    ("143", "Trideptric"),
    ("144", "Zendabo"),
    ("145", "Frightmear"),
    ("146", "Zezimonk"),
    ("147", "Eroarno"),
    ("148", "Infernix"),
    ("149", "Drunagi"),
    ("150", "Shinwin"),
    ("151", "Akuleon"),
    ("152", "Zagathal"),
    ("153", "Boulphyte"),
    ("154", "Howlgus"),
    ("155", "Xiolthan"),
    ("156", "Icthoric"),
    ("157", "Gahnisho"),
    ("158", "Torgalega"),
    ("159", "Nordrian"),
    ("160", "Blizzboon"),
    ("161", "Rhybuto"),
    ("162", "Oboulga"),
    ("163", "Cinbolthrax"),
    ("164", "Oseidro"),
    ("165", "Yuendl"),
    ("166", "Rokusei"),
    ("167", "Rogudora"),
    ("168", "Cheeartic"),
    ("169", "Tormortar"),
    ("170", "Katanakron"),
    ("171", "Narodin"),
    ("172", "Locthos"),
    ("173", "Arcwave"),
    ("174", "Grazlor"),
    ("175", "Skalizard"),
    ("176", "Shikorby"),
    ("177", "Venorat"),
    ("178", "Stomdune"),
    ("179", "Sklyghtning"),
    ("180", "Gilaroc"),
    ("181", "Torfintic"),
    ("182", "Ficesuta"),
    ("183", "Ursalid"),
    ("184", "Ramolgus"),
    ("185", "Volakhan"),
    ("186", "Finorn"),
    ("187", "Frillmilleon"),
    ("188", "Powraroot"),
    ("189", "Narby"),
    ("190", "Pirocean"),
    ("191", "Rairokuma"),
    ("192", "Frovolthon"),
    ("193", "Fanuito"),
    ("194", "Dosfroric"),
    ("195", "Darsignius"),
    ("196", "Hooma"),
    ("197", "Jinmo"),
    ("198", "Trigodrahgon"),
]

# ==========================================
# MAIN APP
# ==========================================

class ChecklistApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Elemental Creatures Checklist")
        self.root.geometry("850x700")

        self.card_vars = {}

        self.load_progress()

        self.dark_mode = self.saved_data.get("dark_mode", False)

        self.set_theme()

        self.create_widgets()

        self.master_set_var.set(
            self.saved_data.get("master_set", False)
        )

        self.populate_cards()

        self.update_progress()

    # ==========================================
    # THEME
    # ==========================================

    def set_theme(self):

        if self.dark_mode:

            self.bg = "#1e1e1e"
            self.fg = "#ffffff"
            self.entry_bg = "#2c2c2c"

        else:

            self.bg = "#f4f4f4"
            self.fg = "#000000"
            self.entry_bg = "#ffffff"

        self.root.configure(bg=self.bg)

    def toggle_theme(self):

        self.dark_mode = not self.dark_mode

        self.set_theme()

        # ROOT AREAS
        self.root.configure(bg=self.bg)
        self.top_frame.configure(bg=self.bg)

        # SEARCH
        self.search_entry.configure(
            bg=self.entry_bg,
            fg=self.fg,
            insertbackground=self.fg
        )

        # LABELS / BUTTONS
        self.progress_label.configure(
            bg=self.bg,
            fg=self.fg
        )

        self.theme_button.configure(
            bg=self.entry_bg,
            fg=self.fg
        )

        self.master_toggle.configure(
            bg=self.bg,
            fg=self.fg,
            selectcolor=self.entry_bg,
            activebackground=self.bg
        )

        # SCROLL AREA
        self.canvas.configure(bg=self.bg)
        self.scrollable_frame.configure(bg=self.bg)

        # REBUILD CARDS
        self.refresh_cards()

        # FORCE REFRESH
        self.canvas.update_idletasks()

        self.save_progress()

    # ==========================================
    # SAVE / LOAD
    # ==========================================

    def load_progress(self):

        if os.path.exists(SAVE_FILE):

            with open(SAVE_FILE, "r") as f:
                self.saved_data = json.load(f)

        else:

            self.saved_data = {
                "dark_mode": False,
                "master_set": False,
                "cards": {}
            }

    def save_progress(self):

        data = {
            "dark_mode": self.dark_mode,
            "master_set": self.master_set_var.get(),
            "cards": {}
        }

        for key, vars_dict in self.card_vars.items():

            data["cards"][key] = {
                "regular": vars_dict["regular"].get(),
                "holo": vars_dict["holo"].get()
            }

        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    # ==========================================
    # UI
    # ==========================================

    def create_widgets(self):

        self.top_frame = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.top_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # PROGRESS LABEL
        self.progress_label = tk.Label(
            self.top_frame,
            text="0%",
            font=("Arial", 14, "bold"),
            bg=self.bg,
            fg=self.fg
        )

        self.progress_label.pack(anchor="w")

        # PROGRESS BAR
        self.progress = ttk.Progressbar(
            self.top_frame,
            orient="horizontal",
            length=500,
            mode="determinate"
        )

        self.progress.pack(fill="x", pady=5)

        # THEME BUTTON
        self.theme_button = tk.Button(
            self.top_frame,
            text="Toggle Theme",
            command=self.toggle_theme,
            bg=self.entry_bg,
            fg=self.fg
        )

        self.theme_button.pack(anchor="e")

        # MASTER SET TOGGLE
        self.master_set_var = tk.BooleanVar()

        self.master_toggle = tk.Checkbutton(
            self.top_frame,
            text="Master Set Mode",
            variable=self.master_set_var,
            command=self.toggle_master_set,
            bg=self.bg,
            fg=self.fg,
            selectcolor=self.entry_bg,
            activebackground=self.bg
        )

        self.master_toggle.pack(anchor="e")

        # SEARCH BAR
        self.search_var = tk.StringVar()

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_cards()
        )

        self.search_entry = tk.Entry(
            self.root,
            textvariable=self.search_var,
            bg=self.entry_bg,
            fg=self.fg,
            insertbackground=self.fg,
            font=("Arial", 12)
        )

        self.search_entry.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        # SCROLL AREA
        self.canvas = tk.Canvas(
            self.root,
            bg=self.bg,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=self.bg
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        # MOUSE WHEEL SCROLL
        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

    # ==========================================
    # SCROLLING
    # ==========================================

    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================================
    # MASTER SET MODE
    # ==========================================

    def toggle_master_set(self):

        self.refresh_cards()

        self.update_progress()

        self.save_progress()

    # ==========================================
    # CARD SETUP
    # ==========================================

    def populate_cards(self):

        for number, name in creatures:

            key = f"{number}-{name}"

            card_data = self.saved_data.get(
                "cards",
                {}
            ).get(key, {})

            regular_val = card_data.get(
                "regular",
                False
            )

            holo_val = card_data.get(
                "holo",
                False
            )

            regular_var = tk.BooleanVar(
                value=regular_val
            )

            holo_var = tk.BooleanVar(
                value=holo_val
            )

            self.card_vars[key] = {
                "regular": regular_var,
                "holo": holo_var
            }

        self.refresh_cards()

    def refresh_cards(self):

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        search_text = self.search_var.get().lower()

        master_mode = self.master_set_var.get()

        for number, name in creatures:

            display_name = f"{number} - {name}"

            key = f"{number}-{name}"

            if search_text not in display_name.lower():
                continue

            row = tk.Frame(
                self.scrollable_frame,
                bg=self.bg
            )

            row.configure(bg=self.bg)

            row.pack(
                fill="x",
                padx=10,
                pady=2
            )

            # CARD LABEL
            label = tk.Label(
                row,
                text=display_name,
                font=("Arial", 11),
                bg=self.bg,
                fg=self.fg,
                anchor="w"
            )

            label.pack(
                side="left",
                fill="x",
                expand=True
            )

            # REGULAR CHECKBOX
            regular_cb = tk.Checkbutton(
                row,
                text="Regular",
                variable=self.card_vars[key]["regular"],
                command=self.on_check,
                bg=self.bg,
                fg=self.fg,
                selectcolor=self.entry_bg,
                activebackground=self.bg
            )

            regular_cb.pack(
                side="right",
                padx=5
            )

            # HOLO CHECKBOX
            if master_mode:

                holo_cb = tk.Checkbutton(
                    row,
                    text="Holo",
                    variable=self.card_vars[key]["holo"],
                    command=self.on_check,
                    bg=self.bg,
                    fg=self.fg,
                    selectcolor=self.entry_bg,
                    activebackground=self.bg
                )

                holo_cb.pack(
                    side="right",
                    padx=5
                )

    # ==========================================
    # PROGRESS
    # ==========================================

    def on_check(self):

        self.update_progress()

        self.save_progress()

    def update_progress(self):

        master_mode = self.master_set_var.get()

        completed = 0

        if master_mode:

            total = len(creatures) * 2

            for vars_dict in self.card_vars.values():

                if vars_dict["regular"].get():
                    completed += 1

                if vars_dict["holo"].get():
                    completed += 1

        else:

            total = len(creatures)

            for vars_dict in self.card_vars.values():

                if vars_dict["regular"].get():
                    completed += 1

        percent = (completed / total) * 100

        self.progress["value"] = percent

        mode_text = (
            "Master Set"
            if master_mode
            else "Regular Set"
        )

        self.progress_label.config(
            text=f"{mode_text}: {completed}/{total} ({percent:.1f}%)"
        )

# ==========================================
# RUN APP
# ==========================================

root = tk.Tk()

app = ChecklistApp(root)

root.mainloop()
