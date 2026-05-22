import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import execute_query

class StazioniFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="📍 Stazioni", font=("Helvetica", 20, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=15)

        # Treeview
        tree_frame = tk.Frame(self, bg="#1e1e2e")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("ID AMAT", "Nome", "ID ARPA", "Inizio Operatività", "Fine Operatività", "Longitudine", "Latitudine")
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

        labels = ["ID AMAT", "Nome", "ID ARPA", "Inizio (YYYY-MM-DD)", "Fine (YYYY-MM-DD)", "Longitudine", "Latitudine"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", bg="#2a2a3e",
                     fg="white", font=("Helvetica", 10)).grid(row=0, column=i*2, padx=6)
            entry = tk.Entry(form_frame, width=13)
            entry.grid(row=0, column=i*2+1, padx=6)
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
        rows = execute_query("SELECT * FROM stazioni ORDER BY nome", fetch=True)
        self.tree.delete(*self.tree.get_children())
        if rows:
            for row in rows:
                self.tree.insert("", "end", values=row)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        labels = ["ID AMAT", "Nome", "ID ARPA", "Inizio (YYYY-MM-DD)", "Fine (YYYY-MM-DD)", "Longitudine", "Latitudine"]
        for label, val in zip(labels, values):
            self.entries[label].delete(0, tk.END)
            self.entries[label].insert(0, val if val else "")

    def inserisci(self):
        try:
            execute_query(
                "INSERT INTO stazioni (id_amat, nome, id_arpa, inizio_operativita, fine_operativita, longitudine, latitudine) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                tuple(self.entries[l].get() for l in ["ID AMAT", "Nome", "ID ARPA", "Inizio (YYYY-MM-DD)", "Fine (YYYY-MM-DD)", "Longitudine", "Latitudine"])
            )
            messagebox.showinfo("✅ Successo", "Stazione inserita!")
            self.carica_dati()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def modifica(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona una riga prima!")
            return
        try:
            execute_query(
                "UPDATE stazioni SET nome=%s, id_arpa=%s, inizio_operativita=%s, fine_operativita=%s, longitudine=%s, latitudine=%s WHERE id_amat=%s",
                (
                    self.entries["Nome"].get(),
                    self.entries["ID ARPA"].get(),
                    self.entries["Inizio (YYYY-MM-DD)"].get(),
                    self.entries["Fine (YYYY-MM-DD)"].get(),
                    self.entries["Longitudine"].get(),
                    self.entries["Latitudine"].get(),
                    self.entries["ID AMAT"].get()
                )
            )
            messagebox.showinfo("✅ Successo", "Stazione aggiornata!")
            self.carica_dati()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def elimina(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona una riga prima!")
            return
        id_amat = self.tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questa stazione?"):
            execute_query("DELETE FROM stazioni WHERE id_amat = %s", (id_amat,))
            messagebox.showinfo("✅ Successo", "Stazione eliminata!")
            self.carica_dati()