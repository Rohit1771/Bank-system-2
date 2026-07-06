# Rohit Bank — Mini Bank System

A full-stack banking web app built with **Flask** and **SQLite**, simulating core banking operations: account creation, login, deposits, withdrawals, peer-to-peer transfers, and transaction history — all backed by a persistent ledger.

## Features

- **User accounts** — register, log in, log out with session-based auth
- **Deposits & withdrawals** — update balance instantly, validated against negative/invalid amounts
- **Transfers** — send money to another registered username, with balance and existence checks
- **Transaction history** — full ledger of every deposit, withdrawal, and transfer, timestamped
- **Profile page** — view account details and current balance
- **Change password** — update credentials after verifying the old password
- **Flash messages** — clear success/error feedback on every action

## Tech Stack

| Layer      | Technology              |
|------------|--------------------------|
| Backend    | Python, Flask             |
| Database   | SQLite (`sqlite3`)        |
| Frontend   | HTML, Jinja2 templates, CSS |
| Fonts      | Fraunces, Inter, IBM Plex Mono (Google Fonts) |

## Project Structure

```
Bank-system/
├── app.py                     # Flask routes and app logic
├── database.py                # Database schema setup
├── bank.db                    # SQLite database
├── static/
│   └── style.css              # Design system (colors, type, components)
└── templates/
    ├── base.html               # Shared layout (header, footer, flash messages)
    ├── index.html               # Landing page
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── deposit.html
    ├── withdraw.html
    ├── transfer.html
    ├── transaction_history.html
    ├── profile.html
    └── change_password.html
```

## Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/Rohit1771/Bank-system.git
   cd Bank-system
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Set up the database** (creates `bank.db` with the required tables)
   ```bash
   python database.py
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. Open `http://localhost:5000` in your browser.

## Design

The UI follows a **"passbook ledger"** theme — deep teal and navy tones, brass accents, a serif display face for headings, and monospace type for all amounts and dates, styled to feel like a real bank ledger rather than a generic template. Every page shares one layout (`base.html`) and one stylesheet (`static/style.css`), so the look stays consistent across the app.

UI and frontend styling for this project were designed with help from **Claude (Anthropic)**.

## Notes

This is a learning/portfolio project built to practice Flask, SQLite, and full-stack web development fundamentals. It is not a real banking application and should not be used to store real financial data.

## Author

**Rohit** — [github.com/Rohit1771](https://github.com/Rohit1771)
