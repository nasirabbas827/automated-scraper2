# Automated-scraper2

A lightweight web‑based application that automates the scraping, storage, and viewing of gig listings. It provides a simple UI for users to register, log in, search, and view detailed gig information.

---

## Overview

`Automated-scraper2` combines a Python backend with HTML templates to:

- Scrape gig data from target websites (configured in `run.py`).
- Store results in a SQLite database (`database.db` / `users.db`).
- Serve a clean, responsive interface for searching and viewing gigs.
- Manage user authentication (register & login).

The project is packaged as a single archive (`Automated-scraper2-finalcode.rar`) for easy distribution.

---

## Features

- **Automated Scraping** – Run the scraper with a single command; results are persisted automatically.  
- **User Management** – Register, log in, and maintain session state.  
- **Search & Filter** – Query gigs by keyword, location, or category.  
- **Detail View** – Click a gig to see full information on a dedicated page.  
- **Responsive UI** – Built with clean HTML templates (`templates/*.html`).  
- **SQLite Persistence** – No external database required; everything lives in `database.db` and `users.db`.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.x (standard library + `sqlite3`) |
| **Frontend** | HTML5 (templates in `templates/`), minimal CSS |
| **Database** | SQLite (`database.db`, `users.db`) |
| **Packaging** | RAR archive (`Automated-scraper2-finalcode.rar`) |

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/Automated-scraper2.git
   cd Automated-scraper2
   ```

2. **Extract the archive** (if you downloaded the `.rar` file)  
   ```bash
   unzip Automated-scraper2-finalcode.rar   # or use your preferred extractor
   ```

3. **Create a virtual environment (recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

4. **Install dependencies** (the project only uses the standard library, but you may need Flask if you extend it)  
   ```bash
   pip install -r requirements.txt   # create this file if you add external packages
   ```

5. **Set up environment variables** (if you use any external APIs)  
   ```bash
   export SCRAPER_API_KEY=YOUR_OWN_API_KEY   # replace with your actual key
   ```

6. **Initialize the databases** (optional – they are already included)  
   ```bash
   python database.py   # creates/updates database.db if needed
   ```

---

## Usage

### Run the scraper & web server

```bash
python run.py
```

- The scraper will start, fetch gig data, and store it in `database.db`.
- A local web server will be launched (default: `http://127.0.0.1:5000`).

### Interact with the application

1. Open a browser and navigate to `http://127.0.0.1:5000`.
2. Register a new account or log in with existing credentials.
3. Use the **Search** page to find gigs.
4. Click a gig to view its full details.

### Development notes

- HTML templates are located in the `templates/` directory:
  - `layout.html` – Base layout shared across pages.
  - `index.html` – Home page.
  - `login.html` / `register.html` – Authentication pages.
  - `search.html` – Search form & results.