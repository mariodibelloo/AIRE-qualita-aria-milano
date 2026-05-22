import tkinter as tk
from tkinter import ttk
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import execute_query

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

class AiFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="🤖 AI / Previsioni", font=("Helvetica", 20, "bold"),
                 bg="#1e1e2e", fg="white").pack(pady=10)

        # Filtri
        filtri_frame = tk.Frame(self, bg="#2a2a3e", pady=8)
        filtri_frame.pack(fill="x", padx=20)

        tk.Label(filtri_frame, text="Inquinante:", bg="#2a2a3e", fg="white").grid(row=0, column=0, padx=8)
        self.filtro_inquinante = ttk.Combobox(filtri_frame, width=12, state="readonly")
        self.filtro_inquinante.grid(row=0, column=1, padx=8)

        tk.Label(filtri_frame, text="Modello:", bg="#2a2a3e", fg="white").grid(row=0, column=2, padx=8)
        self.filtro_modello = ttk.Combobox(filtri_frame, width=18, state="readonly",
                                            values=["Regressione Lineare", "Random Forest"])
        self.filtro_modello.set("Regressione Lineare")
        self.filtro_modello.grid(row=0, column=3, padx=8)

        tk.Button(filtri_frame, text="🚀 Esegui Modello", bg="#a6e3a1", fg="#1e1e2e",
                  font=("Helvetica", 10, "bold"), relief="flat", cursor="hand2",
                  command=self.esegui_modello).grid(row=0, column=4, padx=10)

        # Metriche
        self.metriche_frame = tk.Frame(self, bg="#1e1e2e")
        self.metriche_frame.pack(fill="x", padx=20, pady=5)

        # Area grafico
        self.grafico_frame = tk.Frame(self, bg="#1e1e2e")
        self.grafico_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self._carica_inquinanti()

    def _carica_inquinanti(self):
        rows = execute_query("SELECT nome FROM inquinanti ORDER BY nome", fetch=True)
        if rows:
            nomi = [r[0] for r in rows]
            self.filtro_inquinante["values"] = nomi
            self.filtro_inquinante.set(nomi[0])

    def esegui_modello(self):
        inquinante = self.filtro_inquinante.get()
        modello = self.filtro_modello.get()

        # Carica dati
        rows = execute_query("""
            SELECT m.data, m.stazione_id, m.valore
            FROM misurazioni m
            JOIN inquinanti i ON m.inquinante_id = i.id_inquinante
            WHERE i.nome = %s AND m.valore IS NOT NULL
            ORDER BY m.data
        """, (inquinante,), fetch=True)

        if not rows or len(rows) < 20:
            for w in self.metriche_frame.winfo_children():
                w.destroy()
            tk.Label(self.metriche_frame, text="⚠️ Dati insufficienti per il modello.",
                     bg="#1e1e2e", fg="#f38ba8", font=("Helvetica", 12)).pack()
            return

        # Prepara features
        import pandas as pd
        df = pd.DataFrame(rows, columns=["data", "stazione_id", "valore"])
        df["data"] = pd.to_datetime(df["data"])
        df["giorno_anno"] = df["data"].dt.dayofyear
        df["mese"] = df["data"].dt.month
        df["anno"] = df["data"].dt.year

        X = df[["giorno_anno", "mese", "anno", "stazione_id"]].values
        y = df["valore"].astype(float).values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if modello == "Regressione Lineare":
            model = LinearRegression()
            colore = "#89b4fa"
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            colore = "#a6e3a1"

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        # Mostra metriche
        for w in self.metriche_frame.winfo_children():
            w.destroy()

        metriche_txt = f"Modello: {modello}  |  Inquinante: {inquinante}  |  RMSE: {rmse:.3f}  |  R²: {r2:.3f}  |  Campioni test: {len(y_test)}"
        tk.Label(self.metriche_frame, text=metriche_txt,
                 font=("Helvetica", 11, "bold"), bg="#1e1e2e", fg=colore).pack(pady=5)

        # Grafico reale vs predetto
        for w in self.grafico_frame.winfo_children():
            w.destroy()

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

        # Scatter reale vs predetto
        ax1.scatter(y_test, y_pred, color=colore, alpha=0.6, s=20)
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())
        ax1.plot([min_val, max_val], [min_val, max_val], color="#f38ba8", linewidth=1.5, linestyle="--")
        ax1.set_title(f"{modello} — Reale vs Predetto")
        ax1.set_xlabel("Valore Reale")
        ax1.set_ylabel("Valore Predetto")

        # Distribuzione errori
        errori = y_pred - y_test
        ax2.hist(errori, bins=30, color=colore, edgecolor="#1e1e2e")
        ax2.axvline(0, color="#f38ba8", linewidth=1.5, linestyle="--")
        ax2.set_title("Distribuzione degli Errori")
        ax2.set_xlabel("Errore (Predetto - Reale)")
        ax2.set_ylabel("Frequenza")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)