import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import execute_query

class MisurazioniFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Titolo
        tk.Label(self, text="📊 Misurazioni", font=("Helvetica", 20, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=15)

        # Frame filtri
        filtri_frame = tk.Frame(self, bg="#2a2a3e", pady=10)
        filtri_frame.pack(fill="x", padx=20)

        tk.Label(filtri_frame, text="Stazione ID:", bg="#2a2a3e", fg="white").grid(row=0, column=0, padx=8)
        self.filtro_stazione = tk.Entry(filtri_frame, width=10)
        self.filtro_stazione.grid(row=0, column=1, padx=8)

        tk.Label(filtri_frame, text="Dal:", bg="#2a2a3e", fg="white").grid(row=0, column=2, padx=8)
        self.filtro_dal = tk.Entry(filtri_frame, width=12)
        self.filtro_dal.insert(0, "YYYY-MM-DD")
        self.filtro_dal.grid(row=0, column=3, padx=8)

        tk.Label(filtri_frame, text="Al:", bg="#2a2a3e", fg="white").grid(row=0, column=4, padx=8)
        self.filtro_al = tk.Entry(filtri_frame, width=12)
        self.filtro_al.insert(0, "YYYY-MM-DD")
        self.filtro_al.grid(row=0, column=5, padx=8)

        tk.Label(filtri_frame, text="Inquinante ID:", bg="#2a2a3e", fg="white").grid(row=0, column=6, padx=8)
        self.filtro_inquinante = tk.Entry(filtri_frame, width=10)
        self.filtro_inquinante.grid(row=0, column=7, padx=8)

        tk.Button(filtri_frame, text="🔍 Filtra", bg="#89b4fa", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  command=self.carica_dati).grid(row=0, column=8, padx=10)

        tk.Button(filtri_frame, text="🔄 Reset", bg="#45475a", fg="white",
                  font=("Helvetica", 10), relief="flat", cursor="hand2",
                  command=self.reset_filtri).grid(row=0, column=9, padx=5)

        # Treeview
        tree_frame = tk.Frame(self, bg="#1e1e2e")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("ID", "Stazione", "Data", "Inquinante", "Valore")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#313244", foreground="white",
                        rowheight=28, fieldbackground="#313244", font=("Helvetica", 10))
        style.configure("Treeview.Heading", background="#45475a", foreground="white",
                        font=("Helvetica", 10, "bold"))

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Form CRUD
        form_frame = tk.Frame(self, bg="#2a2a3e", pady=10)
        form_frame.pack(fill="x", padx=20, pady=5)

        labels = ["Stazione ID", "Data (YYYY-MM-DD)", "Inquinante ID", "Valore"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", bg="#2a2a3e",
                     fg="white", font=("Helvetica", 10)).grid(row=0, column=i*2, padx=8)
            entry = tk.Entry(form_frame, width=14)
            entry.grid(row=0, column=i*2+1, padx=8)
            self.entries[label] = entry

        # Bottoni CRUD
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="➕ Inserisci", bg="#a6e3a1", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  width=12, command=self.inserisci).pack(side="left", padx=6)
        tk.Button(btn_frame, text="✏️ Modifica", bg="#89b4fa", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  width=12, command=self.modifica).pack(side="left", padx=6)
        tk.Button(btn_frame, text="🗑️ Elimina", bg="#f38ba8", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  width=12, command=self.elimina).pack(side="left", padx=6)
        tk.Button(btn_frame, text="🔄 Aggiorna", bg="#fab387", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  width=12, command=self.carica_dati).pack(side="left", padx=6)

        self.carica_dati()

    def carica_dati(self):
        query = """
            SELECT m.id_misurazione, s.nome, m.data, i.nome, m.valore
            FROM misurazioni m
            JOIN stazioni s ON m.stazione_id = s.id_amat
            JOIN inquinanti i ON m.inquinante_id = i.id_inquinante
            WHERE 1=1
        """
        params = []

        if self.filtro_stazione.get().strip():
            query += " AND m.stazione_id = %s"
            params.append(self.filtro_stazione.get().strip())

        dal = self.filtro_dal.get().strip()
        al = self.filtro_al.get().strip()
        if dal != "YYYY-MM-DD" and dal:
            query += " AND m.data >= %s"
            params.append(dal)
        if al != "YYYY-MM-DD" and al:
            query += " AND m.data <= %s"
            params.append(al)

        if self.filtro_inquinante.get().strip():
            query += " AND m.inquinante_id = %s"
            params.append(self.filtro_inquinante.get().strip())

        query += " ORDER BY m.data DESC LIMIT 500"

        rows = execute_query(query, params, fetch=True)
        self.tree.delete(*self.tree.get_children())
        if rows:
            for row in rows:
                self.tree.insert("", "end", values=row)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        labels = ["Stazione ID", "Data (YYYY-MM-DD)", "Inquinante ID", "Valore"]
        # Recupera id stazione e inquinante dall'ID misurazione
        row = execute_query(
            "SELECT stazione_id, data, inquinante_id, valore FROM misurazioni WHERE id_misurazione = %s",
            (values[0],), fetch=True
        )
        if row:
            for label, val in zip(labels, row[0]):
                self.entries[label].delete(0, tk.END)
                self.entries[label].insert(0, val)

    def inserisci(self):
        try:
            execute_query(
                "INSERT INTO misurazioni (stazione_id, data, inquinante_id, valore) VALUES (%s, %s, %s, %s)",
                (
                    self.entries["Stazione ID"].get(),
                    self.entries["Data (YYYY-MM-DD)"].get(),
                    self.entries["Inquinante ID"].get(),
                    self.entries["Valore"].get()
                )
            )
            messagebox.showinfo("✅ Successo", "Misurazione inserita!")
            self.carica_dati()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def modifica(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona una riga prima!")
            return
        id_mis = self.tree.item(selected[0])["values"][0]
        try:
            execute_query(
                "UPDATE misurazioni SET stazione_id=%s, data=%s, inquinante_id=%s, valore=%s WHERE id_misurazione=%s",
                (
                    self.entries["Stazione ID"].get(),
                    self.entries["Data (YYYY-MM-DD)"].get(),
                    self.entries["Inquinante ID"].get(),
                    self.entries["Valore"].get(),
                    id_mis
                )
            )
            messagebox.showinfo("✅ Successo", "Misurazione aggiornata!")
            self.carica_dati()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def elimina(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona una riga prima!")
            return
        id_mis = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questa misurazione?"):
            execute_query("DELETE FROM misurazioni WHERE id_misurazione = %s", (id_mis,))
            messagebox.showinfo("✅ Successo", "Misurazione eliminata!")
            self.carica_dati()

    def reset_filtri(self):
        self.filtro_stazione.delete(0, tk.END)
        self.filtro_inquinante.delete(0, tk.END)
        self.filtro_dal.delete(0, tk.END)
        self.filtro_dal.insert(0, "YYYY-MM-DD")
        self.filtro_al.delete(0, tk.END)
        self.filtro_al.insert(0, "YYYY-MM-DD")
        self.carica_dati()