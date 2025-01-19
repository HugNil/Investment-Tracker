import sqlite3

# Anslut till databasen
conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# Skapa tabellen för positioner
def initialize_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        köpDatum DATE DEFAULT (date('now')),
        säljDatum DATE NULL,
        aktie TEXT NOT NULL,
        gav REAL NOT NULL,
        sold REAL NULL,
        stoploss REAL,
        risknivå TEXT CHECK(risknivå IN ('High', 'Medium', 'Low')),
        status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Sold')),
        resultat REAL DEFAULT 0.0
    )
    """)
    conn.commit()


# Lägg till en ny position
def add_position(aktie, gav, stoploss=None, risknivå=None):
    cursor.execute("""
    INSERT INTO positions (aktie, gav, stoploss, risknivå)
    VALUES (?, ?, ?, ?)
    """, (aktie, gav, stoploss, risknivå)
    )
    conn.commit()


# Markera en position som såld och beräkna resultat
def sell_position(id, price=None):
    cursor.execute(
        "SELECT aktie, gav FROM positions WHERE id = ? AND status = 'Active'",
        (id,)
        )
    position = cursor.fetchone()

    if position:
        aktie, gav = position
        if price is not None:
            resultat = ((price - gav) / gav) * 100
        else:
            raise ValueError("Pris måste anges.")

        cursor.execute("""
        UPDATE positions
        SET status = 'Sold', resultat = ?, sold = ?, säljDatum = date('now')
        WHERE id = ?
        """, (round(resultat, 2), price, id)
        )
        conn.commit()
        return aktie, round(resultat, 2)
    return None, None


# Hämta alla aktiva positioner
def get_active_positions():
    cursor.execute(
        "SELECT * FROM positions WHERE status = 'Active'"
        )
    return cursor.fetchall()


# Hämta alla sålda positioner
def get_sold_positions():
    cursor.execute(
        "SELECT * FROM positions WHERE status = 'Sold'"
        )
    return cursor.fetchall()


# Initiera databasen vid import
initialize_database()
