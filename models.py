from datetime import datetime

class Patronne:
    def __init__(self, nom, telephone, marche, produit_principal):
        self.nom = nom
        self.telephone = telephone
        self.marche = marche
        self.produit_principal = produit_principal

class Produit:
    def __init__(self, nom, prix_achat, prix_vente, stock):
        self.nom = nom
        self.prix_achat = prix_achat
        self.prix_vente = prix_vente
        self.stock = stock

class Vente:
    def __init__(self, date, patronne_id, produit_id, quantite, type_paiement):
        self.date = date
        self.patronne_id = patronne_id
        self.produit_id = produit_id
        self.quantite = quantite
        self.type_paiement = type_paiement

class Depense:
    def __init__(self, date, categorie, montant, description):
        self.date = date
        self.categorie = categorie
        self.montant = montant
        self.description = description

class Retrait:
    def __init__(self, date, montant, motif):
        self.date = date
        self.montant = montant
        self.motif = motif