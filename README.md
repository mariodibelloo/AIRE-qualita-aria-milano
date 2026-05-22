# 🌫 AIRE — Qualità dell'Aria a Milano

Applicazione desktop per il monitoraggio e l'analisi della qualità dell'aria a Milano, sviluppata come Project Work finale.

---

## Descrizione

AIRE è un'applicazione Python con interfaccia grafica (Tkinter) che permette di:

- Visualizzare e gestire le misurazioni degli inquinanti atmosferici rilevati dalle stazioni di Milano
- Analizzare i dati tramite grafici interattivi
- Identificare i superamenti dei limiti UE per ogni inquinante
- Applicare modelli di Machine Learning per previsioni sui valori futuri

---

## 🗂 Struttura del Progetto

AIRE-qualita-aria-milano/
├── app/ # Applicazione Tkinter
│ ├── main.py # Entry point e navigazione
│ ├── db.py # Connessione MySQL
│ ├── home.py # Schermata Home
│ ├── misurazioni.py # CRUD Misurazioni
│ ├── grafici.py # Grafici matplotlib
│ ├── superamenti.py # Superamenti limiti UE
│ ├── stazioni.py # CRUD Stazioni
│ └── ai_panel.py # Modelli ML
├── data/
│ ├── raw/ # Dataset originali
│ ├── powerbi/ # CSV per Power BI
│ └── mysql/ # CSV per MySQL
├── db/
│ ├── aire_db.sql # DDL database
│ └── schema_er.png # Schema ER
├── Pulizia/
│ └── ScriptETL.py # Script pulizia dati
├── requirements.txt
└── README.md

---

## 🗄 Database

Il database MySQL `aire_db` è composto da 4 tabelle:

- **stazioni** — stazioni di monitoraggio di Milano
- **inquinanti** — tipologie di inquinanti rilevati
- **stazioni_inquinanti** — relazione N:M tra stazioni e inquinanti
- **misurazioni** — rilevazioni giornaliere per stazione e inquinante

Lo schema ER è disponibile in `db/schema_er.png`.

---

## Installazione

### Requisiti

- Python 3.10+
- MySQL Server

### 1. Clona il repository

```bash
git clone https://github.com/mariodibelloo/AIRE-qualita-aria-milano.git
cd AIRE-qualita-aria-milano
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 3. Configura il database

- Importa `db/aire_db.sql` in MySQL
- Modifica le credenziali in `app/db.py`

### 4. Avvia l'applicazione

```bash
cd app
python main.py
```

---

## 📊 Funzionalità

| Schermata          | Descrizione                                              |
| ------------------ | -------------------------------------------------------- |
| 🏠 Home            | Statistiche generali e navigazione rapida                |
| 📊 Misurazioni     | CRUD completo con filtri per stazione, data e inquinante |
| 📈 Grafici         | Andamento temporale e confronto tra stazioni             |
| ⚠️ Superamenti     | Rilevamento superamenti limiti UE per inquinante         |
| 📍 Stazioni        | CRUD completo delle stazioni di monitoraggio             |
| 🤖 AI / Previsioni | Regressione Lineare e Random Forest sui dati storici     |

---

## Inquinanti monitorati

NO2, PM10, PM2.5, CO, O3, C6H6

---

## Tecnologie utilizzate

- **Python** — linguaggio principale
- **Tkinter** — interfaccia grafica
- **MySQL** — database relazionale
- **Pandas / NumPy** — manipolazione dati
- **Matplotlib** — visualizzazione grafici
- **Scikit-learn** — modelli Machine Learning
- **Power BI** — dashboard di analisi

---

## Autore

Mario Di Belloo — Project Work Generation Visual 2026
