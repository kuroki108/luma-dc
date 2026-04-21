# Luma DC Bot

Ein umfassender Discord-Community-Bot für deutsche Server – gebaut mit discord.py 2.x. Kombiniert ein vollständiges Ticket-System, Selfroles, Bewerbungsmanagement, automatische Willkommensnachrichten und einen Wöchentlichen-Task-Scheduler in einem einzigen Bot.

---

## Features

### 🎫 Ticket-System
- Tickets öffnen per Slash-Command mit Kategorieauswahl (Allgemeiner Support, Technisches Problem, Report)
- Vollständige Ticket-Verwaltung: Add/Remove User, Umbenennen, Schließen
- **HTML-Transkript** bei Ticket-Schließung automatisch per DM zugeschickt
- Logging aller Aktionen in einen dedizierten Log-Channel
- Auto-Delete nach Schließung (konfigurierbar in Sekunden)

### 📝 Bewerbungssystem
- Modal-basierte Teambewerbungen mit 5 Feldern (IGN, Alter, Erfahrung, Aktivität, Motivation)
- Support-Team kann Bewerbungen annehmen, ablehnen oder schließen
- Bewerber erhalten Entscheidung automatisch per DM

### 🎭 Selfroles
- Interaktive Dropdown-Menüs zur Selbst-Rollenvergabe
- 6 Kategorien: **Geschlecht, Alter, Bundesland, DM-Status, Spiele, Ping-Rollen**
- **Exklusive Farbrollen** für Server-Booster
- Persistent – überlebt Bot-Neustarts

### 👋 Willkommensnachrichten
- Automatische Begrüßung im definierten Channel bei Server-Beitritt
- Weist neuen Mitgliedern automatisch Basis-Rollen zu

### 📅 Wöchentlicher Scheduler
- Montags 18:00 Uhr: Wöchentliches Meeting-Post mit ✅/❌-Reaktionen
- Dienstags 17:45 Uhr: 15-Minuten-Erinnerung vor dem Meeting
- Läuft vollautomatisch im Hintergrund (Zeitzone: Europe/Berlin)

---

## Projektstruktur

```
luma-dc/
├── bot.py                    # Einstiegspunkt
├── config.json               # Konfiguration (IDs, Farben, Kategorien)
├── requirements.txt
├── .env                      # Discord Token (nicht ins Repo!)
├── assets/                   # Banner-Bilder für Selfroles
├── modules/
│   ├── selfroles.py          # Dropdown-Menüs für Rollen
│   ├── welcome_msg.py        # Willkommensnachrichten
│   └── weekly.py             # Wöchentlicher Task-Scheduler
└── ticket_system/
    ├── cogs/                 # Slash-Commands
    │   ├── ticket_commands.py
    │   ├── ticket_panel.py
    │   └── application_commands.py
    ├── views/                # UI-Komponenten (Buttons, Modals, Selects)
    │   ├── ticket_views.py
    │   └── application_views.py
    ├── utils/
    │   ├── config.py         # Config-Loader
    │   ├── database.py       # JSON-Datenbank
    │   └── helpers.py        # Hilfsfunktionen
    └── data/
        ├── tickets.json
        └── applications.json
```

---

## Setup

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. `.env` erstellen

```env
DISCORD_TOKEN=dein_bot_token_hier
```

### 3. `config.json` anpassen

| Feld | Beschreibung |
|---|---|
| `prefix` | Prefix für Prefix-Commands (Standard: `!`) |
| `guild_id` | ID deines Discord-Servers |
| `ticket_category_id` | Kategorie-ID für Ticket-Channels |
| `support_role_ids` | Rollen-IDs mit Support-Berechtigung |
| `log_channel_id` | Channel für Log-Nachrichten |
| `delete_closed_after_seconds` | Verzögerung vor Auto-Delete geschlossener Tickets |
| `ticket_categories` | Ticket-Typen (label, emoji, value) |

### 4. Bot starten

```bash
python bot.py
```

### 5. Panel einrichten

Nach dem Start im gewünschten Channel ausführen:

```
/ticket-panel
```

---

## Commands

### Slash-Commands

| Command | Beschreibung | Berechtigung |
|---|---|---|
| `/ticket-panel` | Postet das Ticket-Erstellungs-Panel | Admin |
| `/ticket-bewerbung` | Teambewerbung einreichen | Alle |
| `/ticket-add @user` | User zum Ticket hinzufügen | Support |
| `/ticket-remove @user` | User aus Ticket entfernen | Support |
| `/ticket-rename name` | Ticket-Channel umbenennen | Support |
| `/ticket-close` | Ticket schließen (+ Transkript) | Support / Ersteller |

### Prefix-Commands

| Command | Beschreibung | Berechtigung |
|---|---|---|
| `!selfroles` | Postet das Selfroles-Embed | Admin |
| `!color` | Postet das Booster-Farbrollen-Embed | Admin |
| `!ping` | Pong | Alle |

---

## Technisches

- **Persistenz**: JSON-basiert, kein Datenbank-Server nötig
- **Slash-Commands**: Guild-spezifisch synchronisiert (kein globales Warten)
- **Views**: Persistent – funktionieren nach Bot-Neustart weiterhin
- **Sprache**: Deutsch

---

## Voraussetzungen

- Python 3.10+
- discord.py 2.7.1
- Discord Bot mit den Intents `message_content` und `members`

---

## Entwickler

Erstellt von **Finn** — Python • Discord Bots • IT
