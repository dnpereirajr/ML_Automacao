import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Mercado Livre credentials
    MERCADOLIVRE_EMAIL = os.getenv('MERCADOLIVRE_EMAIL')
    MERCADOLIVRE_PASSWORD = os.getenv('MERCADOLIVRE_PASSWORD')
    
    # Gmail credentials
    GMAIL_EMAIL = os.getenv('GMAIL_EMAIL')
    GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
    
    # WhatsApp settings
    WHATSAPP_PHONE = os.getenv('WHATSAPP_PHONE')
    
    # Affiliate settings
    AFFILIATE_ID = os.getenv('AFFILIATE_ID', 'ML_DEFAULT')
    
    # Search settings
    MAX_PRODUCTS_PER_SEARCH = 20
    CATEGORIES = {
        'eletrônicos': ['smartphone', 'notebook', 'tablet', 'fone', 'tv'],
        'roupas': ['camiseta', 'calça', 'vestido', 'sapato', 'tênis'],
        'casa': ['sofá', 'mesa', 'cadeira', 'cama', 'geladeira'],
        'esportes': ['bicicleta', 'tênis', 'bola', 'academia', 'fitness']
    }
    
    # Email settings
    EMAIL_RECIPIENTS = ['destinatario1@gmail.com', 'destinatario2@gmail.com']
    
    # Notification settings
    ENABLE_EMAIL = os.getenv('ENABLE_EMAIL', 'true').lower() == 'true'
    ENABLE_WHATSAPP = os.getenv('ENABLE_WHATSAPP', 'true').lower() == 'true'
    
    # Schedule settings
    SEND_INTERVAL_HOURS = 1