import re
import tkinter as tk
from tkinter import font as tkfont

BG          = "#020c02"
SURFACE     = "#071007"
BORDER      = "#1a5c1a"
TEXT_PRI    = "#00ff41"
TEXT_SEC    = "#39d939"
ACCENT      = "#00ff41"

WEAK_CLR    = "#ff4444"
MED_CLR     = "#ffcc00"
STRONG_CLR  = "#00dd44"
VSTRONG_CLR = "#00ff41"
COMMON_CLR  = "#ff6600" 

BAR_BG      = "#0d2e0d"
PASS_FG     = "#00ff41"
FAIL_FG     = "#ff4444"


def is_common(password):
    
    pwd = password.lower().strip()


    common_patterns = [
        r'^[a-z]{3,}[0-9]{1,6}$',           # john123
        r'^[a-z]{3,}[@!#$%^&*]+[0-9]*$',    # john@123
        r'^[a-z]{3,}[:;._-]+[0-9]*$',       # john:
        r'^[0-9]{1,6}[a-z]{3,}$',           # 123john
        r'^[@!#$%^&*]+[a-z]{3,}$',          # @john
    ]

    for pattern in common_patterns:
        if re.fullmatch(pattern, pwd):
            return True

    return False
def analyse(password):
    has_min    = len(password) >= 8
    has_long   = len(password) >= 12
    has_upper  = any(c.isupper() for c in password)
    has_digit  = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    common     = is_common(password)

    criteria = [
        ("8+ characters",    has_min),
        ("Uppercase [A-Z]",  has_upper),
        ("Number  [0-9]",    has_digit),
        ("Symbol  (!@#$)",   has_symbol),
        ("12+ characters",   has_long),
        ("Not common/leaked", not common),
    ]

    score = sum(v for _, v in criteria)

    if common:
        strength, color, pct = "COMMON — WEAK", COMMON_CLR, 0.20
    elif not has_min:
        strength, color, pct = "WEAK",          WEAK_CLR,   0.15
    elif score <= 3:
        strength, color, pct = "WEAK",          WEAK_CLR,   0.25
    elif score == 4:
        strength, color, pct = "MEDIUM",        MED_CLR,    0.55
    elif score == 5:
        strength, color, pct = "STRONG",        STRONG_CLR, 0.80
    else:
        strength, color, pct = "VERY STRONG",   VSTRONG_CLR, 1.00

    return strength, color, pct, score, criteria, common


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("[ PASSWORD STRENGTH CHECKER ]")
        self.resizable(True, True)
        self.configure(bg=BG)

        self.f_brand  = tkfont.Font(family="Courier New", size=12, weight="bold")
        self.f_head   = tkfont.Font(family="Courier New", size=18, weight="bold")
        self.f_sub    = tkfont.Font(family="Courier New", size=11)
        self.f_label  = tkfont.Font(family="Courier New", size=13)
        self.f_mono   = tkfont.Font(family="Courier New", size=14)
        self.f_big    = tkfont.Font(family="Courier New", size=28, weight="bold")
        self.f_tip    = tkfont.Font(family="Courier New", size=12)
        self.f_crit   = tkfont.Font(family="Courier New", size=12)
        self.f_btn    = tkfont.Font(family="Courier New", size=12, weight="bold")
        self.f_warn   = tkfont.Font(family="Courier New", size=12, weight="bold")
        self.f_footer = tkfont.Font(family="Courier New", size=10)

        self._show_pwd = False
        self._build_ui()

    def _build_ui(self):
        PAD = 32

        
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=PAD, pady=(PAD, 0))

        tk.Label(hdr, text="PASSWORD STRENGTH CHECKER",
                 font=self.f_head, fg=TEXT_PRI, bg=BG).pack(anchor="w", pady=(4, 0))
        tk.Label(hdr, text=">>  Cyber Security  <<",
                 font=self.f_sub, fg=TEXT_SEC, bg=BG).pack(anchor="w", pady=(4, 0))

        tk.Frame(self, bg=BORDER, height=2).pack(fill="x", padx=PAD, pady=16)

       
        card = tk.Frame(self, bg=SURFACE, bd=0,
                        highlightthickness=2, highlightbackground=BORDER)
        card.pack(fill="x", padx=PAD, pady=(0, 10))

        inner = tk.Frame(card, bg=SURFACE)
        inner.pack(fill="x", padx=22, pady=22)

        tk.Label(inner, text="> Enter password to analyse:",
                 font=self.f_label, fg=TEXT_SEC, bg=SURFACE).pack(anchor="w")

        row = tk.Frame(inner, bg=SURFACE)
        row.pack(fill="x", pady=(8, 0))

        self.pwd_var = tk.StringVar()
        self.pwd_var.trace_add("write", lambda *_: self._update())

        self.entry = tk.Entry(
            row, textvariable=self.pwd_var, show="*",
            font=self.f_mono, bg="#000d00", fg=TEXT_PRI,
            insertbackground=ACCENT, relief="flat",
            bd=0, highlightthickness=2,
            highlightbackground=BORDER, highlightcolor=ACCENT,
            width=30
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

        self.eye_btn = tk.Button(
            row, text="SHOW", font=self.f_btn,
            bg=BORDER, fg=TEXT_PRI,
            activebackground=ACCENT, activeforeground=BG,
            relief="flat", bd=0, cursor="hand2",
            command=self._toggle_show,
            padx=14, pady=6
        )
        self.eye_btn.pack(side="left")
        self.entry.focus_set()


        self.common_banner = tk.Label(
            inner,
            text="",
            font=self.f_warn,
            fg=COMMON_CLR, bg=SURFACE,
            anchor="w", justify="left"
        )
        self.common_banner.pack(fill="x", pady=(10, 0))

        
        bar_frame = tk.Frame(inner, bg=SURFACE)
        bar_frame.pack(fill="x", pady=(10, 0))

        self.strength_lbl = tk.Label(
            bar_frame, text="AWAITING INPUT...",
            font=self.f_big, fg=TEXT_SEC, bg=SURFACE, anchor="w"
        )
        self.strength_lbl.pack(side="left")

        self.score_lbl = tk.Label(
            bar_frame, text="", font=self.f_label,
            fg=TEXT_SEC, bg=SURFACE, anchor="e"
        )
        self.score_lbl.pack(side="right", anchor="s", pady=6)

        bar_track = tk.Frame(inner, bg=BAR_BG, height=12)
        bar_track.pack(fill="x", pady=(8, 0))
        bar_track.pack_propagate(False)

        self.bar_fill = tk.Frame(bar_track, bg=TEXT_SEC, height=12)
        self.bar_fill.place(x=0, y=0, relheight=1, relwidth=0)

        
        self.tip_lbl = tk.Label(
            inner, text="", font=self.f_tip,
            fg=TEXT_SEC, bg=SURFACE,
            wraplength=620, justify="left", anchor="w"
        )
        self.tip_lbl.pack(fill="x", pady=(10, 0))

        tk.Frame(card, bg=BORDER, height=2).pack(fill="x")

    
        grid_frame = tk.Frame(card, bg=SURFACE)
        grid_frame.pack(fill="x", padx=22, pady=18)

        tk.Label(grid_frame, text="> Security criteria:",
                 font=self.f_label, fg=TEXT_SEC, bg=SURFACE
                 ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        self.crit_labels = []
        criteria_names = [
            "8+ characters",    "Uppercase [A-Z]",  "Number  [0-9]",
            "Symbol  (!@#$)",   "12+ characters",   "Not common/leaked",
        ]
        for i, name in enumerate(criteria_names):
            col   = i % 3
            row_n = (i // 3) + 1
            cell  = tk.Frame(grid_frame, bg=SURFACE)
            cell.grid(row=row_n, column=col, sticky="w", padx=(0, 30), pady=5)

            dot = tk.Label(cell, text="[ ]", font=self.f_crit, fg=BORDER, bg=SURFACE)
            dot.pack(side="left")
            lbl = tk.Label(cell, text=f"  {name}", font=self.f_crit, fg=TEXT_SEC, bg=SURFACE)
            lbl.pack(side="left")
            self.crit_labels.append((dot, lbl))

        tk.Frame(self, bg=BORDER, height=2).pack(fill="x", padx=PAD)
        tk.Label(
            self,
            text="> Designed dy: Danish ",
            font=self.f_footer, fg=TEXT_SEC, bg=BG
        ).pack(pady=(8, PAD))

        self.update_idletasks()
        self.geometry("720x660")

    def _toggle_show(self):
        self._show_pwd = not self._show_pwd
        self.entry.config(show="" if self._show_pwd else "*")
        self.eye_btn.config(text="HIDE" if self._show_pwd else "SHOW")

    def _update(self):
        pwd = self.pwd_var.get()

        if not pwd:
            self.strength_lbl.config(text="AWAITING INPUT...", fg=TEXT_SEC)
            self.score_lbl.config(text="")
            self.bar_fill.place(relwidth=0)
            self.tip_lbl.config(text="")
            self.common_banner.config(text="")
            for dot, lbl in self.crit_labels:
                dot.config(text="[ ]", fg=BORDER)
                lbl.config(fg=TEXT_SEC)
            return

        strength, color, pct, score, criteria, common = analyse(pwd)

        if common:
            self.common_banner.config(
                text="⚠  ALERT: This password appears in known leaked password databases!\n"
                     "   Attackers will try it first. Choose something unique.",
                fg=COMMON_CLR
            )
        else:
            self.common_banner.config(text="")

        self.strength_lbl.config(text=strength, fg=color)
        self.score_lbl.config(text=f"SCORE: {score}/6", fg=TEXT_SEC)
        self.bar_fill.config(bg=color)
        self.bar_fill.place(relwidth=pct)

        tips = {
            "COMMON — WEAK": ">  BREACH RISK: Found in leaked password lists. Change immediately.",
            "WEAK":          ">  WARNING: Too weak. Add uppercase, numbers and symbols.",
            "MEDIUM":        ">  NOTICE:  Getting there! Add one more type or use 12+ chars.",
            "STRONG":        ">  INFO:    Strong! Use 12+ characters for maximum security.",
            "VERY STRONG":   ">  PASS:    Excellent — all security criteria met.",
        }
        self.tip_lbl.config(text=tips[strength], fg=color)

        for (dot, lbl), (_, passed) in zip(self.crit_labels, criteria):
            if passed:
                dot.config(text="[+]", fg=PASS_FG)
                lbl.config(fg=PASS_FG)
            else:
                dot.config(text="[x]", fg=FAIL_FG)
                lbl.config(fg=FAIL_FG)

if __name__ == "__main__":
    app = App()
    app.mainloop()