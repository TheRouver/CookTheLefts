# CookTheLefts - Recipe Search Web Application

CookTheLefts ist eine Flask-basierte Webanwendung, die es Benutzern ermöglicht, Rezepte basierend auf vorhandenen Zutaten zu finden. Die Anwendung nutzt die Spoonacular API für Rezeptvorschläge und ermöglicht es Benutzern auch, eigene Rezepte zu teilen.

## Systemanforderungen

### Windows
- Python 3.8 - 3.11 (getestet auf 3.8, 3.9, 3.10, 3.11)
- Visual Studio Code
- Git (optional, für Versionskontrolle)
- 500 MB freier Speicherplatz
- Windows 10/11

### macOS
- Python 3.11
- Xcode Command Line Tools
- Visual Studio Code
- Git (optional)
- 500 MB freier Speicherplatz
- macOS 11 (Big Sur) oder höher

### Linux
- Python 3.8 - 3.11
- python3-venv Paket
- Visual Studio Code
- Git (optional)
- 500 MB freier Speicherplatz
- Ubuntu 20.04/22.04, Debian 11/12 oder vergleichbar

## Installation nach Betriebssystem

### Windows Installation

1. **Python installieren**
   - Python von [python.org](https://www.python.org/downloads/) herunterladen
   - Bei der Installation "Add Python to PATH" auswählen
   - Installation mit `python --version` überprüfen

2. **Visual Studio Code**
   - VSCode von [code.visualstudio.com](https://code.visualstudio.com/) installieren
   - Empfohlene Extensions:
     - Python (Microsoft)
     - Python Extension Pack
     - SQLite Viewer

3. **Projekt einrichten**
   ```batch
   :: Repository klonen (oder ZIP herunterladen)
   git clone [repository-url]
   cd CookTheLefts

   :: Virtuelle Umgebung erstellen
   python -m venv venv

   :: Virtuelle Umgebung aktivieren
   venv\Scripts\activate

   :: Abhängigkeiten installieren
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

### macOS Installation

1. **Xcode Command Line Tools installieren**
   ```bash
   xcode-select --install
   ```

2. **Python installieren**
   ```bash
   # Mit Homebrew
   brew install python@3.11

   # Oder von python.org
   # Laden Sie Python von https://www.python.org/downloads/ herunter
   ```

3. **Visual Studio Code**
   - VSCode von [code.visualstudio.com](https://code.visualstudio.com/) installieren
   - Empfohlene Extensions wie bei Windows

4. **Projekt einrichten**
   ```bash
   # Repository klonen
   git clone [repository-url]
   cd CookTheLefts

   # Virtuelle Umgebung erstellen
   python3 -m venv venv

   # Virtuelle Umgebung aktivieren
   source venv/bin/activate

   # Abhängigkeiten installieren
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   ```


### Linux Installation

1. **Erforderliche Pakete installieren**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git

   # Fedora
   sudo dnf install python3 python3-pip python3-virtualenv git
   ```

2. **Visual Studio Code**
   ```bash
   # Ubuntu/Debian
   sudo apt install code

   # Fedora
   sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
   sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
   sudo dnf install code
   ```

3. **Projekt einrichten**
   ```bash
   # Repository klonen
   git clone [repository-url]
   cd CookTheLefts

   # Virtuelle Umgebung erstellen
   python3 -m venv venv

   # Virtuelle Umgebung aktivieren
   source venv/bin/activate

   # Abhängigkeiten installieren
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   ```

## Projekt in Visual Studio Code starten

### Detaillierte Anleitung für Visual Studio Code

1. **Projekt in VS Code öffnen**
   - Öffnen Sie VS Code
   - Gehen Sie zu `File > Open Folder` (Windows) oder `File > Open` (macOS)
   - Wählen Sie den CookTheLefts Projektordner aus

2. **Python Extension installieren**
   - Öffnen Sie die Extensions-Ansicht (`Strg+Shift+X` auf Windows, `Cmd+Shift+X` auf macOS)
   - Suchen Sie nach "Python"
   - Installieren Sie die offizielle Python Extension von Microsoft

3. **Python Interpreter auswählen**
   - Drücken Sie `Strg+Shift+P` (Windows) oder `Cmd+Shift+P` (macOS)
   - Geben Sie "Python: Select Interpreter" ein
   - Wählen Sie die Python-Version aus dem venv-Ordner aus (z.B. `./venv/Scripts/python.exe` auf Windows oder `./venv/bin/python` auf macOS)

4. **Terminal öffnen und virtuelle Umgebung aktivieren**
   - Öffnen Sie ein neues Terminal in VS Code (`Strg+Shift+` auf Windows, `Cmd+Shift+` auf macOS)
   - Die virtuelle Umgebung sollte automatisch aktiviert werden
   - Falls nicht, aktivieren Sie sie manuell:
     ```bash
     # Windows
     .\venv\Scripts\activate
     
     # macOS
     source venv/bin/activate
     ```

5. **Datenbank initialisieren**
   ```bash
   # Windows
   flask db upgrade
   
   # macOS
   python3 -m flask db upgrade
   ```

6. **Projekt ausführen**
   - Öffnen Sie `run.py` in VS Code
   - Klicken Sie auf den "Play" Button oben rechts oder
   - Drücken Sie `F5` zum Debuggen oder
   - Nutzen Sie das Terminal:
     ```bash
     # Windows
     python run.py
     
     # macOS
     python3 run.py
     ```

Die Anwendung ist nun unter [http://127.0.0.1:5000](http://127.0.0.1:5000) erreichbar.

## Alternative Startmethoden

### Methode 1: Über das Terminal

1. **VSCode öffnen**
   ```bash
   code .
   ```

2. **Terminal in VSCode öffnen**
   - Windows: `Strg+Shift+P`
   - macOS: `Cmd+Shift+P`
   - Linux: `Ctrl+Shift+P`
   Dann "Terminal: Create New Terminal" auswählen

3. **Virtuelle Umgebung aktivieren**
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

4. **Datenbank initialisieren**
   ```bash
   # Windows
   flask db upgrade

   # macOS/Linux
   python3 -m flask db upgrade
   ```

5. **Anwendung starten**
   ```bash
   # Windows
   python run.py

   # macOS/Linux
   python3 run.py
   ```

Die Anwendung ist dann unter [http://127.0.0.1:5000](http://127.0.0.1:5000) erreichbar.

### Methode 2: Über VS Code Kontextmenü

1. **Virtuelle Umgebung aktivieren** (falls noch nicht aktiviert)
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **In VS Code:**
   - Rechtsklick auf `run.py` im Datei-Explorer
   - "Open in Integrated Terminal" auswählen
   - Im Terminal eingeben:
     ```bash
     # Windows
     python run.py

     # macOS/Linux
     python3 run.py
     ```

Die Anwendung ist dann ebenfalls unter [http://127.0.0.1:5000](http://127.0.0.1:5000) erreichbar.

## API-Konfiguration

### Spoonacular API
Die Anwendung verwendet die Spoonacular API für Rezeptvorschläge. Um die API nutzen zu können:

1. Registrieren Sie sich auf [Spoonacular](https://spoonacular.com/food-api) für einen API-Schlüssel
2. Erstellen Sie eine `.env` Datei im Hauptverzeichnis:
   ```
   SPOONACULAR_API_KEY=Ihr_API_Schlüssel
   ```

## Projektstruktur

Die Anwendung folgt einer modularen Flask-Architektur mit klarer Trennung der Verantwortlichkeiten:

### Kernkomponenten
```
CookTheLefts/
├── run.py                # Haupteinstiegspunkt der Anwendung - Startet den Flask-Server
├── config.py             # Zentrale Konfigurationsdatei - Enthält alle Umgebungsvariablen und Einstellungen
└── requirements.txt      # Liste aller Python-Abhängigkeiten mit exakten Versionen
```

### Anwendungsmodule (app/)
```
app/
├── __init__.py          # Initialisiert die Flask-Anwendung, Datenbank und Erweiterungen
├── models.py            # Definiert SQLAlchemy Datenbankmodelle (User, Recipe, Comment, etc.)
│
├── auth/               # Authentifizierungs- und Autorisierungsmodul
│   ├── forms.py        # WTForms Klassen für Login/Registrierung
│   └── routes.py       # Routen für Benutzeranmeldung, Registrierung und Abmeldung
│
├── main/               # Hauptmodul für allgemeine Seiten
│   └── routes.py       # Routen für Startseite, Über uns, Impressum
│
├── recipes/            # Kernmodul für Rezeptverwaltung
│   ├── forms.py        # Formulare für Rezepterstellung und -bearbeitung
│   └── routes.py       # Routen für CRUD-Operationen von Rezepten
│
├── services/           # Externe Dienste und APIs
│   └── meal_api.py     # Integration mit Spoonacular API für Rezeptvorschläge
│
├── static/            # Statische Ressourcen
│   ├── css/           # Stylesheets für das Frontend
│   ├── js/            # JavaScript-Dateien für interaktive Funktionen
│   ├── images/        # Bildressourcen
│   └── uploads/       # Speicherort für hochgeladene Benutzerbilder
│
└── templates/         # Jinja2 HTML-Templates
    ├── base.html      # Basis-Template mit gemeinsamer Struktur
    ├── auth/          # Templates für Login/Registrierung
    ├── main/          # Templates für Hauptseiten
    └── recipes/       # Templates für Rezeptverwaltung
```

### Datenbankkomponenten
```
├── instance/           # Instanzordner für lokale Daten
│   └── cookthelefts.db # SQLite Datenbank mit allen Anwendungsdaten
│
└── migrations/         # Alembic Datenbank-Migrationen
    └── versions/      # Migrationsskripte für Datenbankänderungen
```

### Hauptfunktionen der Module

- **auth**: Verwaltet die Benutzerauthentifizierung und -sitzungen
  - Registrierung neuer Benutzer
  - Login/Logout-Funktionalität
  - Passwort-Hashing und Validierung

- **main**: Stellt die grundlegenden Seiten und Navigation bereit
  - Startseite mit Suchfunktion
  - Statische Seiten (Über uns, Impressum)
  - Navigation und Grundlayout

- **recipes**: Kernfunktionalität für Rezeptverwaltung
  - Erstellen, Bearbeiten, Löschen von Rezepten
  - Rezeptsuche und -filterung
  - Bewertungen und Kommentare
  - Integration mit Spoonacular API

- **services**: Externe Dienstintegrationen
  - Spoonacular API-Anbindung für Rezeptsuche und -vorschläge
  - Verarbeitung von API-Antworten und Zutatenlisten

- **models**: Zentrale Datenbankmodelle
  - User: Benutzerdaten und Authentifizierung
  - Recipe: Rezeptinformationen und Metadaten
  - Comment: Benutzerkommentare zu Rezepten
  - Rating: Bewertungssystem für Rezepte

## Fehlerbehebung

### Windows-spezifische Probleme
1. **Python nicht im PATH**
   - Python neu installieren und "Add Python to PATH" auswählen
   - Oder Python manuell zum PATH hinzufügen

2. **Berechtigungsprobleme**
   - PowerShell als Administrator ausführen
   - Execution Policy anpassen: `Set-ExecutionPolicy RemoteSigned`

### macOS-spezifische Probleme
1. **Python-Version-Konflikt**
   ```bash
   # Prüfen Sie die aktive Python-Version
   python3 --version
   
   # Bei Bedarf eine spezifische Version verwenden
   python3.11 -m venv venv
   ```

2. **Berechtigungsprobleme**
   ```bash
   sudo chown -R $(whoami) venv/
   chmod +x run.py
   ```

### Linux-spezifische Probleme
1. **Fehlende Pakete**
   ```bash
   sudo apt install python3-dev default-libmysqlclient-dev build-essential
   # oder
   sudo dnf install python3-devel mysql-devel gcc
   ```

2. **SQLite Probleme**
   ```bash
   sudo apt install sqlite3
   # oder
   sudo dnf install sqlite
   ```

## Entwickelt von

- Yakub Sileman
- Alexey Kirchner
- Abdulhamid Suliman

Für den Kurs "E-Business und digitale Geschäftsmodelle" an der Hochschule für Wirtschaft und Recht Berlin.
