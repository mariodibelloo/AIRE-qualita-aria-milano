import tkinter as tk
from tkinter import ttk
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import execute_query

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraficiFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="📈 Grafici", font=("Helvetica", 20, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=10)

        # Filtri
        filtri_frame = tk.Frame(self, bg="#2a2a3e", pady=8)
        filtri_frame.pack(fill="x", padx=20)

        tk.Label(filtri_frame, text="Inquinante:", bg="#2a2a3e", fg="white").grid(row=0, column=0, padx=8)
        self.filtro_inquinante = ttk.Combobox(filtri_frame, width=12, state="readonly")
        self.filtro_inquinante.grid(row=0, column=1, padx=8)

        tk.Label(filtri_frame, text="Stazione ID:", bg="#2a2a3e", fg="white").grid(row=0, column=2, padx=8)
        self.filtro_stazione = tk.Entry(filtri_frame, width=10)
        self.filtro_stazione.grid(row=0, column=3, padx=8)

        tk.Label(filtri_frame, text="Dal:", bg="#2a2a3e", fg="white").grid(row=0, column=4, padx=8)
        self.filtro_dal = tk.Entry(filtri_frame, width=12)
        self.filtro_dal.insert(0, "2025-01-01")
        self.filtro_dal.grid(row=0, column=5, padx=8)

        tk.Label(filtri_frame, text="Al:", bg="#2a2a3e", fg="white").grid(row=0, column=6, padx=8)
        self.filtro_al = tk.Entry(filtri_frame, width=12)
        self.filtro_al.insert(0, "2025-12-31")
        self.filtro_al.grid(row=0, column=7, padx=8)

        tk.Button(filtri_frame, text="📊 Genera Grafici", bg="#89b4fa", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  command=self.genera_grafici).grid(row=0, column=8, padx=10)

        # Area grafici
        self.grafici_frame = tk.Frame(self, bg="#1e1e2e")
        self.grafici_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self._carica_inquinanti()
        self.genera_grafici()

    def _carica_inquinanti(self):
        rows = execute_query("SELECT nome FROM inquinanti ORDER BY nome", fetch=True)
        if rows:
            nomi = [r[0] for r in rows]
            self.filtro_inquinante["values"] = nomi
            self.filtro_inquinante.set(nomi[0])

    def genera_grafici(self):
        # Pulisci grafici precedenti
        for widget in self.grafici_frame.winfo_children():
            widget.destroy()

        inquinante = self.filtro_inquinante.get()
        stazione = self.filtro_stazione.get().strip()
        dal = self.filtro_dal.get().strip()
        al = self.filtro_al.get().strip()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
        fig.patch.set_facecolor("#1e1e2e")

        for ax in (ax1, ax2):
            ax.set_facecolor("#313244")
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")
            for spine in ax.spines.values():
                spine.set_edgecolor("#45475a")

        # --- Grafico 1: Andamento temporale ---
        query1 = """
            SELECT m.data, AVG(m.valore)
            FROM misurazioni m
            JOIN inquinanti i ON m.inquinante_id = i.id_inquinante
            WHERE i.nome = %s AND m.data BETWEEN %s AND %s
        """
        params1 = [inquinante, dal, al]
        if stazione:
            query1 += " AND m.stazione_id = %s"
            params1.append(stazione)
        query1 += " GROUP BY m.data ORDER BY m.data"

        rows1 = execute_query(query1, params1, fetch=True)
        if rows1:
            date = [str(r[0]) for r in rows1]
            valori = [float(r[1]) for r in rows1]
            ax1.plot(date, valori, color="#89b4fa", linewidth=1.5)
            ax1.set_title(f"Andamento {inquinante} nel tempo")
            ax1.set_xlabel("Data")
            ax1.set_ylabel("Valore medio")
            step = max(1, len(date) // 8)
            ax1.set_xticks(range(0, len(date), step))
            ax1.set_xticklabels([date[i] for i in range(0, len(date), step)], rotation=45, ha="right", fontsize=8)
        else:
            ax1.text(0.5, 0.5, "Nessun dato", ha="center", va="center", color="white")
            ax1.set_title(f"Andamento {inquinante} nel tempo")

        # --- Grafico 2: Confronto tra stazioni ---
        rows2 = execute_query("""
            SELECT s.nome, AVG(m.valore)
            FROM misurazioni m
            JOIN stazioni s ON m.stazione_id = s.id_amat
            JOIN inquinanti i ON m.inquinante_id = i.id_inquinante
            WHERE i.nome = %s AND m.data BETWEEN %s AND %s
            GROUP BY s.nome
            ORDER BY AVG(m.valore) DESC
        """, (inquinante, dal, al), fetch=True)

        if rows2:
            stazioni = [r[0] for r in rows2]
            medie = [float(r[1]) for r in rows2]
            bars = ax2.bar(stazioni, medie, color="#a6e3a1")
            ax2.set_title(f"Confronto stazioni — {inquinante}")
            ax2.set_xlabel("Stazione")
            ax2.set_ylabel("Valore medio")
            ax2.set_xticklabels(stazioni, rotation=45, ha="right", fontsize=8)
            for bar, val in zip(bars, medie):
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                         f"{val:.1f}", ha="center", va="bottom", color="white", fontsize=8)
        else:
            ax2.text(0.5, 0.5, "Nessun dato", ha="center", va="center", color="white")
            ax2.set_title(f"Confronto stazioni — {inquinante}")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.grafici_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)