import tkinter as tk
from tkinter import ttk
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import execute_query

LIMITI_UE = {
    "NO2":   40.0,
    "PM10":  40.0,
    "PM2.5": 25.0,
    "CO_8h": 10000.0,
    "O3":    120.0,
    "C6H6":  5.0,
}

class SuperamentiFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="⚠️ Superamenti Limiti UE", font=("Helvetica", 20, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=15)

        # Filtri
        filtri_frame = tk.Frame(self, bg="#2a2a3e", pady=10)
        filtri_frame.pack(fill="x", padx=20)

        tk.Label(filtri_frame, text="Inquinante:", bg="#2a2a3e", fg="white").grid(row=0, column=0, padx=8)
        self.filtro_inquinante = ttk.Combobox(filtri_frame, values=list(LIMITI_UE.keys()), width=12, state="readonly")
        self.filtro_inquinante.grid(row=0, column=1, padx=8)
        self.filtro_inquinante.set("NO2")

        tk.Label(filtri_frame, text="Dal:", bg="#2a2a3e", fg="white").grid(row=0, column=2, padx=8)
        self.filtro_dal = tk.Entry(filtri_frame, width=12)
        self.filtro_dal.insert(0, "2024-01-01")
        self.filtro_dal.grid(row=0, column=3, padx=8)

        tk.Label(filtri_frame, text="Al:", bg="#2a2a3e", fg="white").grid(row=0, column=4, padx=8)
        self.filtro_al = tk.Entry(filtri_frame, width=12)
        self.filtro_al.insert(0, "2025-12-31")
        self.filtro_al.grid(row=0, column=5, padx=8)

        tk.Button(filtri_frame, text="🔍 Cerca", bg="#89b4fa", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  command=self.carica_dati).grid(row=0, column=6, padx=10)

        # KPI contatore
        self.lbl_count = tk.Label(self, text="", font=("Helvetica", 13, "bold"),
                                   bg="#1e1e2e", fg="#f38ba8")
        self.lbl_count.pack(pady=5)

        # Treeview
        tree_frame = tk.Frame(self, bg="#1e1e2e")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("Data", "Stazione", "Inquinante", "Valore", "Limite UE", "Superamento")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=18)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#313244", foreground="white",
                        rowheight=28, fieldbackground="#313244", font=("Helvetica", 10))
        style.configure("Treeview.Heading", background="#45475a", foreground="white",
                        font=("Helvetica", 10, "bold"))
        style.map("Treeview", background=[("selected", "#f38ba8")])

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.carica_dati()

    def carica_dati(self):
        nome_inq = self.filtro_inquinante.get()
        limite = LIMITI_UE.get(nome_inq, 0)
        dal = self.filtro_dal.get().strip()
        al = self.filtro_al.get().strip()

        rows = execute_query("""
            SELECT m.data, s.nome, i.nome, m.valore
            FROM misurazioni m
            JOIN stazioni s ON m.stazione_id = s.id_amat
            JOIN inquinanti i ON m.inquinante_id = i.id_inquinante
            WHERE i.nome = %s AND m.valore > %s AND m.data BETWEEN %s AND %s
            ORDER BY m.valore DESC
        """, (nome_inq, limite, dal, al), fetch=True)

        self.tree.delete(*self.tree.get_children())
        count = 0
        if rows:
            for row in rows:
                data, stazione, inquinante, valore = row
                superamento = f"+{float(valore) - limite:.2f}"
                self.tree.insert("", "end", values=(data, stazione, inquinante, valore, limite, superamento))
                count += 1

        self.lbl_count.config(text=f"⚠️ Totale superamenti trovati: {count}  |  Limite UE {nome_inq}: {limite}")