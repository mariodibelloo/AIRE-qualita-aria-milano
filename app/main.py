import tkinter as tk
from tkinter import ttk
from home import HomeFrame
from misurazioni import MisurazioniFrame
from grafici import GraficiFrame
from superamenti import SuperamentiFrame
from stazioni import StazioniFrame
from ai_panel import AiFrame
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

SCREENS = {
    "Home": HomeFrame,
    "Misurazioni": MisurazioniFrame,
    "Grafici": GraficiFrame,
    "Superamenti": SuperamentiFrame,
    "Stazioni": StazioniFrame,
    "AI / Previsioni": AiFrame,
}

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AIRE — Qualità dell'Aria a Milano")
        self.geometry("1200x700")
        self.configure(bg="#1e1e2e")
        self._build_ui()
        self.show_frame("Home")

    def _build_ui(self):
        # Sidebar sinistra
        sidebar = tk.Frame(self, bg="#2a2a3e", width=180)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🌫 AIRE", font=("Helvetica", 16, "bold"),
                 bg="#2a2a3e", fg="#a6e3a1").pack(pady=30)

        for name in SCREENS:
            btn = tk.Button(
                sidebar, text=name, font=("Helvetica", 11),
                bg="#2a2a3e", fg="white", activebackground="#45475a",
                activeforeground="white", relief="flat", cursor="hand2",
                command=lambda n=name: self.show_frame(n)
            )
            btn.pack(fill="x", padx=10, pady=4, ipady=8)

        # Area contenuto principale
        self.container = tk.Frame(self, bg="#1e1e2e")
        self.container.pack(side="right", fill="both", expand=True)

        self.frames = {}
        for name, FrameClass in SCREENS.items():
            frame = FrameClass(self.container, self)
            self.frames[name] = frame
            frame.place(relwidth=1, relheight=1)

    def show_frame(self, name):
        self.frames[name].tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()