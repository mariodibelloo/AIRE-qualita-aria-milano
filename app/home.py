import tkinter as tk
from tkinter import ttk
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import execute_query

class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Titolo principale
        tk.Label(self, text="🌫 AIRE", font=("Helvetica", 36, "bold"),
                 bg="#1e1e2e", fg="#a6e3a1").pack(pady=20)
        tk.Label(self, text="Qualità dell'Aria a Milano",
                 font=("Helvetica", 16), bg="#1e1e2e", fg="#cdd6f4").pack()
        tk.Label(self, text="Sistema di monitoraggio e analisi degli inquinanti atmosferici",
                 font=("Helvetica", 11), bg="#1e1e2e", fg="#6c7086").pack(pady=5)

        # Separatore
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=40, pady=20)

        # Card statistiche
        stats_frame = tk.Frame(self, bg="#1e1e2e")
        stats_frame.pack(pady=10)

        stats = self._get_stats()
        cards = [
            ("📍 Stazioni", stats["stazioni"], "#89b4fa"),
            ("🧪 Inquinanti", stats["inquinanti"], "#a6e3a1"),
            ("📊 Misurazioni", stats["misurazioni"], "#fab387"),
            ("⚠️ Superamenti NO2", stats["superamenti"], "#f38ba8"),
        ]

        for i, (label, valore, colore) in enumerate(cards):
            card = tk.Frame(stats_frame, bg="#2a2a3e", width=200, height=120)
            card.grid(row=0, column=i, padx=15, pady=10)
            card.pack_propagate(False)

            tk.Label(card, text=label, font=("Helvetica", 11),
                     bg="#2a2a3e", fg="#cdd6f4").pack(pady=(18, 5))
            tk.Label(card, text=str(valore), font=("Helvetica", 26, "bold"),
                     bg="#2a2a3e", fg=colore).pack()

        # Separatore
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=40, pady=20)

        # Ultima misurazione
        tk.Label(self, text="📅 Ultima misurazione registrata",
                 font=("Helvetica", 12, "bold"), bg="#1e1e2e", fg="white").pack()

        ultima = self._get_ultima_misurazione()
        if ultima:
            data, stazione, inquinante, valore = ultima
            tk.Label(self, text=f"{data}  —  {stazione}  —  {inquinante}: {valore}",
                     font=("Helvetica", 12), bg="#1e1e2e", fg="#cdd6f4").pack(pady=8)

        # Bottoni navigazione rapida
        tk.Label(self, text="Vai a:", font=("Helvetica", 11),
                 bg="#1e1e2e", fg="#6c7086").pack(pady=(20, 5))

        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack()

        schermate = [
            ("📊 Misurazioni", "Misurazioni"),
            ("📈 Grafici", "Grafici"),
            ("⚠️ Superamenti", "Superamenti"),
            ("📍 Stazioni", "Stazioni"),
        ]

        for label, screen in schermate:
            tk.Button(btn_frame, text=label, font=("Helvetica", 10, "bold"),
                      bg="#45475a", fg="white", relief="flat", cursor="hand2",
                      width=16, pady=8,
                      command=lambda s=screen: controller.show_frame(s)).pack(side="left", padx=8)

    def _get_stats(self):
        s = execute_query("SELECT COUNT(*) FROM stazioni", fetch=True)
        i = execute_query("SELECT COUNT(*) FROM inquinanti", fetch=True)
        m = execute_query("SELECT COUNT(*) FROM misurazioni", fetch=True)
        sup = execute_query("""
            SELECT COUNT(*) FROM misurazioni m
            JOIN inquinanti i ON m.inquinante_id = i.id_inquinante
            WHERE i.nome = 'NO2' AND m.valore > 40
        """, fetch=True)
        return {
            "stazioni":    s[0][0] if s else 0,
            "inquinanti":  i[0][0] if i else 0,
            "misurazioni": m[0][0] if m else 0,
            "superamenti": sup[0][0] if sup else 0,
        }

    def _get_ultima_misurazione(self):
        rows = execute_query("""
            SELECT m.data, s.nome, i.nome, m.valore
            FROM misurazioni m
            JOIN stazioni s ON m.stazione_id = s.id_amat
            JOIN inquinanti i ON m.inquinante_id = i.id_inquinante
            ORDER BY m.data DESC LIMIT 1
        """, fetch=True)
        return rows[0] if rows else None