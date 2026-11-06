# -*- coding: utf-8 -*-
"""
Daily English Desktop Widget
Windows 10/11 | Python 3.10+
Run: python english_widget.py
"""
import json, os, random, sys, tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

ROOT = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, "quotes.json")
BG = "#172333"
CARD = "#203247"
ACCENT = "#67B7F7"
FG = "#F4F7FB"
MUTED = "#A9B8C9"

class EnglishWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily English")
        self.root.geometry("390x500+80+100")
        self.root.minsize(330, 420)
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 0.96)
        self.quotes = self.load_quotes()
        self.category = "全部"
        self.current = None
        self.last_hour = None
        self.show_translation = True
        self.show_example = False
        self.drag_x = self.drag_y = 0
        self.build_ui()
        self.refresh(force=True)
        self.tick()

    def load_quotes(self):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if data else []
        except Exception as e:
            messagebox.showerror("素材库读取失败", f"无法读取 quotes.json：\\n{e}")
            return []

    def build_ui(self):
        # Header / drag area
        header = tk.Frame(self.root, bg=BG, height=42)
        header.pack(fill="x", padx=15, pady=(10, 4))
        header.pack_propagate(False)
        title = tk.Label(header, text="✦  DAILY ENGLISH", bg=BG, fg=ACCENT,
                         font=("Segoe UI", 10, "bold"))
        title.pack(side="left", anchor="center")
        close = tk.Label(header, text="×", bg=BG, fg=MUTED, cursor="hand2",
                         font=("Segoe UI", 18))
        close.pack(side="right", padx=(8, 0))
        close.bind("<Button-1>", lambda e: self.root.destroy())
        mini = tk.Label(header, text="—", bg=BG, fg=MUTED, cursor="hand2",
                        font=("Segoe UI", 15))
        mini.pack(side="right")
        mini.bind("<Button-1>", lambda e: self.root.iconify())
        for w in (header, title):
            w.bind("<ButtonPress-1>", self.start_move)
            w.bind("<B1-Motion>", self.do_move)

        self.clock = tk.Label(self.root, text="", bg=BG, fg=MUTED,
                              font=("Segoe UI", 9))
        self.clock.pack(anchor="w", padx=18, pady=(0, 8))

        self.panel = tk.Frame(self.root, bg=CARD, highlightthickness=1,
                              highlightbackground="#30465D")
        self.panel.pack(fill="both", expand=True, padx=12, pady=4)

        self.category_var = tk.StringVar(value="全部")
        bar = tk.Frame(self.panel, bg=CARD)
        bar.pack(fill="x", padx=14, pady=(14, 6))
        tk.Label(bar, text="学习主题", bg=CARD, fg=MUTED,
                 font=("Segoe UI", 9)).pack(side="left")
        self.combo = ttk.Combobox(bar, textvariable=self.category_var,
                                  state="readonly", width=13,
                                  values=["全部"] + sorted(set(q["category"] for q in self.quotes)))
        self.combo.pack(side="right")
        self.combo.bind("<<ComboboxSelected>>", self.change_category)

        self.english = tk.Label(self.panel, text="", bg=CARD, fg=FG,
                                font=("Georgia", 19, "bold"), wraplength=325,
                                justify="left", anchor="w")
        self.english.pack(fill="x", padx=17, pady=(20, 12))

        self.chinese = tk.Label(self.panel, text="", bg=CARD, fg="#D5E0EC",
                                font=("Microsoft YaHei UI", 11), wraplength=325,
                                justify="left", anchor="w")
        self.chinese.pack(fill="x", padx=17, pady=(0, 18))

        tk.Frame(self.panel, bg="#3B5065", height=1).pack(fill="x", padx=17)
        vocab = tk.Frame(self.panel, bg=CARD)
        vocab.pack(fill="x", padx=17, pady=(15, 3))
        tk.Label(vocab, text="TODAY'S WORD", bg=CARD, fg=ACCENT,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.word = tk.Label(vocab, text="", bg=CARD, fg=FG,
                             font=("Segoe UI", 17, "bold"))
        self.word.pack(anchor="w", pady=(4, 0))
        self.phonetic = tk.Label(vocab, text="", bg=CARD, fg=MUTED,
                                 font=("Segoe UI", 10))
        self.phonetic.pack(anchor="w")
        self.meaning = tk.Label(vocab, text="", bg=CARD, fg="#D5E0EC",
                                font=("Microsoft YaHei UI", 10))
        self.meaning.pack(anchor="w", pady=(3, 0))

        self.example_box = tk.Frame(self.panel, bg=CARD)
        self.example = tk.Label(self.example_box, text="", bg=CARD, fg=FG,
                                font=("Segoe UI", 10), wraplength=320,
                                justify="left")
        self.example.pack(anchor="w", pady=(8, 2))
        self.example_cn = tk.Label(self.example_box, text="", bg=CARD, fg=MUTED,
                                   font=("Microsoft YaHei UI", 9), wraplength=320,
                                   justify="left")
        self.example_cn.pack(anchor="w")

        actions = tk.Frame(self.panel, bg=CARD)
        actions.pack(side="bottom", fill="x", padx=14, pady=13)
        self.translation_btn = tk.Button(actions, text="隐藏翻译", command=self.toggle_translation,
                                         bg="#304A63", fg=FG, relief="flat",
                                         activebackground="#3A5A78", activeforeground=FG,
                                         font=("Microsoft YaHei UI", 9), padx=8, pady=5)
        self.translation_btn.pack(side="left")
        self.example_btn = tk.Button(actions, text="例句", command=self.toggle_example,
                                     bg="#304A63", fg=FG, relief="flat",
                                     activebackground="#3A5A78", activeforeground=FG,
                                     font=("Microsoft YaHei UI", 9), padx=12, pady=5)
        self.example_btn.pack(side="left", padx=7)
        self.next_btn = tk.Button(actions, text="换一句  ↻", command=lambda: self.refresh(force=True),
                                  bg=ACCENT, fg="#102033", relief="flat",
                                  activebackground="#8BC9FA", activeforeground="#102033",
                                  font=("Microsoft YaHei UI", 9, "bold"), padx=12, pady=5)
        self.next_btn.pack(side="right")

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=16, pady=(5, 9))
        tk.Label(footer, text="拖动顶部移动 · 每小时自动更新", bg=BG, fg=MUTED,
                 font=("Microsoft YaHei UI", 8)).pack(side="left")
        self.opacity_btn = tk.Label(footer, text="透明度", bg=BG, fg=MUTED,
                                    cursor="hand2", font=("Microsoft YaHei UI", 8))
        self.opacity_btn.pack(side="right")
        self.opacity_btn.bind("<Button-1>", self.cycle_opacity)

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Control-n>", lambda e: self.refresh(force=True))

    def start_move(self, event):
        self.drag_x, self.drag_y = event.x_root - self.root.winfo_x(), event.y_root - self.root.winfo_y()

    def do_move(self, event):
        self.root.geometry(f"+{event.x_root-self.drag_x}+{event.y_root-self.drag_y}")

    def change_category(self, _=None):
        self.category = self.category_var.get()
        self.refresh(force=True)

    def refresh(self, force=False):
        available = [q for q in self.quotes if self.category == "全部" or q["category"] == self.category]
        if not available:
            return
        if force or self.current not in available:
            choices = [q for q in available if q != self.current]
            self.current = random.choice(choices or available)
        q = self.current
        self.english.config(text=q["english"])
        self.chinese.config(text=q["chinese"])
        self.word.config(text=q["word"])
        self.phonetic.config(text=q["phonetic"])
        self.meaning.config(text=q["meaning"])
        self.example.config(text=q["example"])
        self.example_cn.config(text=q["example_cn"])
        self.last_hour = datetime.now().strftime("%Y-%m-%d %H")
        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        self.clock.config(text=f"{now.strftime('%A, %d %B')}   ·   {now.strftime('%H:%M')}")

    def tick(self):
        now_hour = datetime.now().strftime("%Y-%m-%d %H")
        self.update_clock()
        if self.last_hour and now_hour != self.last_hour:
            self.refresh(force=True)
        self.root.after(15000, self.tick)

    def toggle_translation(self):
        self.show_translation = not self.show_translation
        if self.show_translation:
            self.chinese.pack(fill="x", padx=17, pady=(0, 18))
            self.translation_btn.config(text="隐藏翻译")
        else:
            self.chinese.pack_forget()
            self.translation_btn.config(text="显示翻译")

    def toggle_example(self):
        self.show_example = not self.show_example
        if self.show_example:
            self.example_box.pack(fill="x", padx=17, pady=(4, 0), before=self.panel.winfo_children()[-1])
            self.example_btn.config(text="收起例句")
        else:
            self.example_box.pack_forget()
            self.example_btn.config(text="例句")

    def cycle_opacity(self, _=None):
        current = float(self.root.attributes("-alpha"))
        levels = [0.96, 0.85, 0.72, 1.0]
        next_level = next((x for x in levels if x < current - 0.01), 1.0)
        self.root.attributes("-alpha", next_level)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnglishWidget(root)
    root.mainloop()
