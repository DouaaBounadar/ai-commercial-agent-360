import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# TABLE 1 : Prospect
class Prospect(Base):
    __tablename__ = 'prospect'
    prospect_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom = Column(String(255))
    telephone = Column(String(20), unique=True)
    email = Column(String(255))
    entreprise = Column(String(255))
    source = Column(String(50)) # WhatsApp/Email/Form/Chat
    status = Column(String(50)) # Nouveau/Qualifié/Client/Perdu
    date_premiere_contact = Column(DateTime)
    date_creation = Column(DateTime, default=datetime.utcnow)

# TABLE 3 : Produit
class Produit(Base):
    __tablename__ = 'produit'
    produit_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), unique=True)
    categorie = Column(String(100)) # Nacelle Ciseaux/Verticale/etc.
    caracteristiques = Column(JSONB) # {hauteur, énergie, tarifs, etc.}
    stock_disponible = Column(Integer)
    date_creation = Column(DateTime, default=datetime.utcnow)

# TABLE 4 : Devis
class Devis(Base):
    __tablename__ = 'devis'
    devis_id = Column(String(20), primary_key=True) # Format: DEV-2026-001
    prospect_id = Column(UUID(as_uuid=True), ForeignKey('prospect.prospect_id', ondelete='CASCADE'))
    produit_id = Column(Integer, ForeignKey('produit.produit_id'))
    caracteristiques_choisies = Column(JSONB) # Équipement, durée, etc.
    duree = Column(String(50))
    quantite = Column(Integer)
    prix_unitaire = Column(Numeric(10, 2))
    prix_total = Column(Numeric(10, 2))
    tva = Column(Numeric(10, 2))
    frais_livraison = Column(Numeric(10, 2))
    montant_caution = Column(Numeric(10, 2))
    prix_total_ttc = Column(Numeric(10, 2))
    pdf_path = Column(String(255))
    status = Column(String(50)) # Brouillon/Envoyé/Accepté/Rejeté
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_envoi = Column(DateTime)
    date_limite_acceptation = Column(DateTime)
    date_acceptation = Column(DateTime)
    date_rejet = Column(DateTime)
    motif_rejet = Column(Text)