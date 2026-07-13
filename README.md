# 💙 SOUFFLE V2.0 - Système de Gestion pour les Mamans Vendeuses

**Une WebApp responsive pour gérer les ventes, dépenses et finances des femmes du marché**

## 🏪 À propos

Souffle V2.0 est une application web simple et accessible conçue pour aider les femmes du marché à gérer leurs finances personnelles et professionnelles. L'application tourne directement dans le navigateur sur smartphone, tablette ou ordinateur.

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.7+
- pip (gestionnaire de paquets Python)

### Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/1er-Reel/souffle-v2-Owner-prof-et-gardien.git
cd souffle-v2-Owner-prof-et-gardien

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python app.py
```

### Accès

Ouvrez votre navigateur et allez à:
```
http://localhost:5000
```

## 📱 Utilisation sur Téléphone (Redmi ou autre)

### Sur le même réseau WiFi

1. **Trouvez votre adresse IP locale:**
   - Windows: Ouvrir CMD et tapez `ipconfig` → cherchez "IPv4 Address"
   - Mac/Linux: Ouvrir Terminal et tapez `ifconfig` → cherchez l'IP

2. **Lancez l'application:**
   ```bash
   python app.py
   ```
   Vous verrez: `Running on http://0.0.0.0:5000`

3. **Sur votre téléphone:**
   - Connectez-vous au même WiFi que votre ordinateur
   - Ouvrez le navigateur
   - Allez à: `http://VOTRE_IP:5000`

### Exemple avec Redmi
```
Si votre IP est 192.168.1.50:
http://192.168.1.50:5000
```

## 📊 Fonctionnalités - Étape 1

### Dashboard
- 📅 Bénéfice du jour
- 📈 Bénéfice du mois
- 🏦 Argent retirable
- 💸 Bouton pour retirer de l'argent

### Enregistrer une Vente
- ➕ Sélectionner un produit
- Entrer la quantité
- Choisir le mode de paiement (Cash/Crédit)
- Confirmer la vente

### Base de Données
- 📦 5 tables SQLite (Patronnes, Produits, Ventes, Dépenses, Retraits)
- 💾 Stockage local en .db
- 🔄 Synchronisation automatique

## 💰 Formules de Calcul

```
Bénéfice_Brut = Somme(ventes.quantite × (prix_vente - prix_achat))
Bénéfice_Net = Bénéfice_Brut - Somme(dépenses.montant)
Argent_Retirable = Bénéfice_Net - Somme(retraits.montant)
```

## 🎨 Design

- 🔵 Couleurs: Bleu + Blanc
- 📱 Gros boutons tactiles
- 📝 Texte grand et lisible
- 📱 Responsive sur tous les appareils
- 🇫🇷 100% en français

## 📦 Structure du Projet

```
souffle-v2/
├── app.py                 # Serveur Flask principal
├── database.py            # Configuration SQLite
├── models.py              # Modèles de données
├── requirements.txt       # Dépendances Python
├── database.db            # Base de données (créée automatiquement)
├── templates/
│   ├── base.html         # Template de base
│   ├── dashboard.html    # Dashboard
│   └── vente.html        # Enregistrer une vente
└── static/
    ├── css/
    │   └── style.css     # Styles CSS
    └── js/
        └── app.js        # Logique frontend
```

## 📋 Roadmap

- [x] **Étape 1**: Dashboard + Ventes + Retraits
- [ ] **Étape 2**: Gestion Produits + Dépenses
- [ ] **Étape 3**: Rapports PDF
- [ ] **Étape 4**: Historique complet

## 🛠️ Technologies

- **Backend**: Python + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript Vanilla
- **Database**: SQLite
- **Devise**: XOF (Franc CFA)

## 📞 Support

En cas de problème, vérifiez:
1. Que Python 3.7+ est installé
2. Que les dépendances sont installées: `pip install -r requirements.txt`
3. Que le port 5000 est disponible
4. L'adresse IP correcte pour l'accès mobile

## 📄 Licence

Ce projet est créé pour les femmes du marché. Libre d'utilisation.

---

**Créé avec 💙 pour les Mamans Vendeuses**