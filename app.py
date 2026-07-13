from flask import Flask, render_template, request, jsonify, g
from database import init_db, get_db, close_db
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

# Initialiser la base de données au démarrage
with app.app_context():
    init_db()

# Fermer la DB à la fin de chaque requête
app.teardown_appcontext(close_db)

# ===== ROUTES DASHBOARD =====
@app.route('/')
def dashboard():
    """Page principale avec résumé du jour et du mois"""
    db = get_db()
    
    # Bénéfice du jour
    benefice_jour = calculate_benefice('jour', db)
    
    # Bénéfice du mois
    benefice_mois = calculate_benefice('mois', db)
    
    # Argent retirable
    argent_retirable = calculate_argent_retirable(db)
    
    return render_template('dashboard.html', 
                         benefice_jour=benefice_jour,
                         benefice_mois=benefice_mois,
                         argent_retirable=argent_retirable)

# ===== ROUTES VENTES =====
@app.route('/vente', methods=['GET'])
def page_vente():
    """Page pour enregistrer une vente"""
    db = get_db()
    cursor = db.cursor()
    
    # Charger les produits disponibles
    cursor.execute('SELECT id, nom, prix_vente, stock FROM produits WHERE stock > 0 ORDER BY nom')
    produits = cursor.fetchall()
    
    return render_template('vente.html', produits=produits)

@app.route('/api/vente', methods=['POST'])
def enregistrer_vente():
    """API pour enregistrer une vente"""
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    try:
        produit_id = data.get('produit_id')
        quantite = int(data.get('quantite'))
        type_paiement = data.get('type_paiement', 'cash')
        
        # Vérifier le stock
        cursor.execute('SELECT stock, prix_achat, prix_vente FROM produits WHERE id = ?', (produit_id,))
        produit = cursor.fetchone()
        
        if not produit or produit[0] < quantite:
            return jsonify({'success': False, 'message': 'Stock insuffisant'}), 400
        
        # Enregistrer la vente
        cursor.execute('''
            INSERT INTO ventes (date, patronne_id, produit_id, quantite, type_paiement)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1, produit_id, quantite, type_paiement))
        
        # Mettre à jour le stock
        nouveau_stock = produit[0] - quantite
        cursor.execute('UPDATE produits SET stock = ? WHERE id = ?', (nouveau_stock, produit_id))
        
        db.commit()
        
        return jsonify({'success': True, 'message': 'Vente enregistrée avec succès'})
    
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ===== ROUTES RETRAITS =====
@app.route('/api/retrait', methods=['POST'])
def enregistrer_retrait():
    """API pour retirer de l'argent"""
    data = request.json
    db = get_db()
    cursor = db.cursor()
    
    try:
        montant = float(data.get('montant'))
        motif = data.get('motif', 'maison')
        
        # Vérifier l'argent disponible
        argent_retirable = calculate_argent_retirable(db)
        
        if montant > argent_retirable:
            return jsonify({'success': False, 'message': 'Montant insuffisant disponible'}), 400
        
        # Enregistrer le retrait
        cursor.execute('''
            INSERT INTO retraits (date, montant, motif)
            VALUES (?, ?, ?)
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), montant, motif))
        
        db.commit()
        
        return jsonify({'success': True, 'message': 'Retrait effectué avec succès'})
    
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ===== FONCTIONS UTILITAIRES =====
def calculate_benefice(periode, db):
    """Calcule le bénéfice net selon la période"""
    cursor = db.cursor()
    
    if periode == 'jour':
        date_filter = "DATE(ventes.date) = DATE('now')"
        depense_filter = "DATE(depenses.date) = DATE('now')"
    else:  # mois
        date_filter = "strftime('%Y-%m', ventes.date) = strftime('%Y-%m', 'now')"
        depense_filter = "strftime('%Y-%m', depenses.date) = strftime('%Y-%m', 'now')"
    
    # Bénéfice brut
    query_benefice = f'''
        SELECT COALESCE(SUM(v.quantite * (p.prix_vente - p.prix_achat)), 0)
        FROM ventes v
        JOIN produits p ON v.produit_id = p.id
        WHERE {date_filter}
    '''
    cursor.execute(query_benefice)
    benefice_brut = cursor.fetchone()[0]
    
    # Somme des dépenses
    query_depenses = f'''
        SELECT COALESCE(SUM(montant), 0)
        FROM depenses
        WHERE {depense_filter}
    '''
    cursor.execute(query_depenses)
    total_depenses = cursor.fetchone()[0]
    
    benefice_net = benefice_brut - total_depenses
    
    return max(0, benefice_net)

def calculate_argent_retirable(db):
    """Calcule l'argent disponible pour retrait"""
    cursor = db.cursor()
    
    # Bénéfice net total
    cursor.execute('''
        SELECT COALESCE(SUM(v.quantite * (p.prix_vente - p.prix_achat)), 0)
        FROM ventes v
        JOIN produits p ON v.produit_id = p.id
    ''')
    benefice_brut = cursor.fetchone()[0]
    
    # Total dépenses
    cursor.execute('SELECT COALESCE(SUM(montant), 0) FROM depenses')
    total_depenses = cursor.fetchone()[0]
    
    # Total retraits
    cursor.execute('SELECT COALESCE(SUM(montant), 0) FROM retraits')
    total_retraits = cursor.fetchone()[0]
    
    benefice_net = benefice_brut - total_depenses
    argent_retirable = benefice_net - total_retraits
    
    return max(0, argent_retirable)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)