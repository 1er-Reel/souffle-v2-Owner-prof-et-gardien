import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    """Récupère la connexion à la base de données"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    """Ferme la connexion"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialise la base de données avec les tables"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    
    # Table Patronnes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patronnes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            telephone TEXT,
            marche TEXT,
            produit_principal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table Produits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix_achat REAL NOT NULL,
            prix_vente REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table Ventes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP NOT NULL,
            patronne_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            type_paiement TEXT CHECK(type_paiement IN ('cash', 'credit')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patronne_id) REFERENCES patronnes(id),
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        )
    ''')
    
    # Table Dépenses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS depenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP NOT NULL,
            categorie TEXT CHECK(categorie IN ('transport', 'sac', 'maison')),
            montant REAL NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table Retraits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS retraits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP NOT NULL,
            montant REAL NOT NULL,
            motif TEXT CHECK(motif IN ('maison', 'reinvestir', 'soins_gardien')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table Solidarité (NOUVELLE)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solidarite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP NOT NULL,
            motif TEXT CHECK(motif IN ('orphelinat', 'aide')),
            montant REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insérer une patronne par défaut
    cursor.execute('''
        INSERT OR IGNORE INTO patronnes (id, nom, telephone, marche, produit_principal)
        VALUES (1, 'Maman Souffle', '221XX XXX XXXX', 'Marché', 'Produits Locaux')
    ''')
    
    # Insérer des produits d'exemple
    produits_exemple = [
        ('Riz', 500, 600, 100),
        ('Huile', 800, 1000, 50),
        ('Sel', 200, 300, 200),
        ('Sucre', 1000, 1200, 75),
    ]
    
    for nom, prix_achat, prix_vente, stock in produits_exemple:
        cursor.execute('''
            INSERT OR IGNORE INTO produits (nom, prix_achat, prix_vente, stock)
            VALUES (?, ?, ?, ?)
        ''', (nom, prix_achat, prix_vente, stock))
    
    db.commit()
    db.close()
