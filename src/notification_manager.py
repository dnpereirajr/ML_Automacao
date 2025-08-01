import yagmail
import pywhatkit as kit
from datetime import datetime
from typing import List
import logging
from jinja2 import Template

from .models import Product
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self):
        self.gmail_client = None
        self.setup_gmail()
    
    def setup_gmail(self):
        """Configura cliente Gmail"""
        try:
            if Config.GMAIL_EMAIL and Config.GMAIL_PASSWORD:
                self.gmail_client = yagmail.SMTP(
                    Config.GMAIL_EMAIL, 
                    Config.GMAIL_PASSWORD
                )
                logger.info("Cliente Gmail configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar Gmail: {e}")
    
    def send_email(self, products: List[Product]):
        """Envia email com todos os produtos"""
        try:
            if not Config.ENABLE_EMAIL:
                logger.info("Envio por email desabilitado")
                return True
                
            if not self.gmail_client or not products:
                return False
            
            html_content = self._generate_email_html(products)
            subject = f"🔥 {len(products)} Ofertas Imperdíveis - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            
            self.gmail_client.send(
                to=Config.EMAIL_RECIPIENTS,
                subject=subject,
                contents=html_content
            )
            
            logger.info(f"Email enviado para {len(Config.EMAIL_RECIPIENTS)} destinatários")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")
            return False
    
    def send_whatsapp_messages(self, products: List[Product]):
        """Envia mensagens separadas por produto no WhatsApp"""
        try:
            if not Config.ENABLE_WHATSAPP:
                logger.info("Envio por WhatsApp desabilitado")
                return True
                
            if not Config.WHATSAPP_PHONE or not products:
                return False
            
            phone = Config.WHATSAPP_PHONE.replace('+', '').replace(' ', '')
            
            for i, product in enumerate(products):
                message = self._format_whatsapp_message(product)
                
                # Calcula horário de envio (com intervalo de 2 minutos entre mensagens)
                now = datetime.now()
                send_time = now.replace(
                    hour=now.hour,
                    minute=now.minute + (i * 2),
                    second=0
                )
                
                kit.sendwhatmsg(
                    phone_no=phone,
                    message=message,
                    time_hour=send_time.hour,
                    time_min=send_time.minute,
                    wait_time=15,
                    tab_close=True
                )
                
                logger.info(f"WhatsApp agendado para produto: {product.title[:50]}...")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar WhatsApp: {e}")
            return False
    
    def _generate_email_html(self, products: List[Product]) -> str:
        """Gera HTML moderno e elegante para email"""
        template_str = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Ofertas Especiais</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }
                .header {
                    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }
                .header h1 {
                    margin: 0;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .subtitle {
                    margin: 10px 0 0 0;
                    font-size: 1.2em;
                    opacity: 0.9;
                }
                .products {
                    padding: 20px;
                }
                .product {
                    border: 1px solid #eee;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    padding: 20px;
                    background: #fafafa;
                    transition: transform 0.3s ease;
                }
                .product:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }
                .product-title {
                    font-size: 1.3em;
                    font-weight: bold;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .price-section {
                    margin: 15px 0;
                }
                .original-price {
                    text-decoration: line-through;
                    color: #888;
                    font-size: 1.1em;
                }
                .current-price {
                    color: #e74c3c;
                    font-size: 1.5em;
                    font-weight: bold;
                    margin-left: 10px;
                }
                .discount-badge {
                    background: #e74c3c;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 15px;
                    font-size: 0.9em;
                    margin-left: 10px;
                }
                .product-info {
                    margin: 10px 0;
                    color: #666;
                }
                .buy-button {
                    display: inline-block;
                    background: linear-gradient(45deg, #4CAF50, #45a049);
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    margin-top: 15px;
                    transition: all 0.3s ease;
                }
                .buy-button:hover {
                    transform: scale(1.05);
                    box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
                }
                .footer {
                    background: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 20px;
                    font-size: 0.9em;
                }
                .category-tag {
                    background: #3498db;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 10px;
                    font-size: 0.8em;
                    margin-right: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔥 Ofertas Especiais</h1>
                    <div class="subtitle">{{ products|length }} produtos selecionados especialmente para você!</div>
                    <div class="subtitle">{{ current_time }}</div>
                </div>
                
                <div class="products">
                    {% for product in products %}
                    <div class="product">
                        <div class="product-title">
                            <span class="category-tag">{{ product.category.title() }}</span>
                            {{ product.title }}
                        </div>
                        
                        <div class="price-section">
                            {% if product.discount_percentage > 0 %}
                            <span class="original-price">De R$ {{ "%.2f"|format(product.original_price) }}</span>
                            <span class="current-price">Por R$ {{ "%.2f"|format(product.current_price) }}</span>
                            <span class="discount-badge">-{{ "%.0f"|format(product.discount_percentage) }}%</span>
                            {% else %}
                            <span class="current-price">R$ {{ "%.2f"|format(product.current_price) }}</span>
                            {% endif %}
                        </div>
                        
                        <div class="product-info">
                            <div>💳 {{ product.payment_options }}</div>
                            <div>🚚 {{ product.shipping_info }}</div>
                            <div>{{ product.feedback_score }}</div>
                        </div>
                        
                        <a href="{{ product.affiliate_url }}" class="buy-button">
                            📲 COMPRAR AGORA
                        </a>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="footer">
                    <p>Sistema Automatizado de Ofertas • {{ current_time }}</p>
                    <p>Este é um email automático. Aproveite as ofertas!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        template = Template(template_str)
        return template.render(
            products=products,
            current_time=datetime.now().strftime('%d/%m/%Y às %H:%M')
        )
    
    def _format_whatsapp_message(self, product: Product) -> str:
        """Formata mensagem para WhatsApp"""
        emoji_map = {
            'eletrônicos': '📱',
            'roupas': '👕',
            'casa': '🏠',
            'esportes': '⚽',
            'outros': '🛒'
        }
        
        emoji = emoji_map.get(product.category, '🛒')
        
        message = f"""🔥 *OFERTA ESPECIAL* {emoji}

*{product.title}*

"""
        
        if product.discount_percentage > 0:
            message += f"""💰 ~De R$ {product.original_price:.2f}~
💸 *Por R$ {product.current_price:.2f}*
🏷️ *Desconto de {product.discount_percentage:.0f}%*

"""
        else:
            message += f"💰 *R$ {product.current_price:.2f}*\n\n"
        
        message += f"""💳 {product.payment_options}
🚚 {product.shipping_info}
{product.feedback_score}

📲 *LINK DE COMPRA* ⬇️
{product.affiliate_url}

_Oferta por tempo limitado!_ ⏰"""
        
        return message