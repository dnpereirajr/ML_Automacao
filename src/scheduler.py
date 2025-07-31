import schedule
import time
import logging
from datetime import datetime
from typing import List
import threading

from .scraper import MercadoLivreScraper
from .notification_manager import NotificationManager
from .models import Product
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutomationScheduler:
    def __init__(self):
        self.scraper = MercadoLivreScraper()
        self.notification_manager = NotificationManager()
        self.is_running = False
        self.thread = None
    
    def search_all_products(self) -> List[Product]:
        """Busca produtos em todas as categorias"""
        all_products = []
        
        # Login no Mercado Livre
        if not self.scraper.login(Config.MERCADOLIVRE_EMAIL, Config.MERCADOLIVRE_PASSWORD):
            logger.error("Falha no login. Continuando sem login...")
        
        # Busca produtos em promoção
        logger.info("Buscando produtos em promoção...")
        for category, keywords in Config.CATEGORIES.items():
            for keyword in keywords[:2]:  # Limita para evitar muitas requisições
                try:
                    result = self.scraper.search_products(keyword, is_promotion=True)
                    all_products.extend(result.products)
                    logger.info(f"Encontrados {len(result.products)} produtos em promoção para '{keyword}'")
                    time.sleep(2)  # Pausa entre requisições
                except Exception as e:
                    logger.error(f"Erro ao buscar {keyword}: {e}")
        
        # Busca alguns produtos normais
        logger.info("Buscando produtos normais...")
        popular_searches = ['iphone', 'notebook', 'tênis', 'camiseta']
        for search_term in popular_searches:
            try:
                result = self.scraper.search_products(search_term, is_promotion=False)
                # Pega apenas os 5 primeiros de cada categoria
                all_products.extend(result.products[:5])
                logger.info(f"Encontrados {len(result.products[:5])} produtos normais para '{search_term}'")
                time.sleep(2)  # Pausa entre requisições
            except Exception as e:
                logger.error(f"Erro ao buscar {search_term}: {e}")
        
        # Remove duplicatas baseado no título
        unique_products = []
        seen_titles = set()
        for product in all_products:
            if product.title not in seen_titles:
                unique_products.append(product)
                seen_titles.add(product.title)
        
        logger.info(f"Total de produtos únicos encontrados: {len(unique_products)}")
        return unique_products
    
    def send_notifications(self):
        """Executa o ciclo completo de busca e envio"""
        logger.info(f"Iniciando ciclo de busca e envio - {datetime.now()}")
        
        try:
            # Busca produtos
            products = self.search_all_products()
            
            if not products:
                logger.warning("Nenhum produto encontrado")
                return
            
            # Ordena por desconto (maiores descontos primeiro)
            products.sort(key=lambda x: x.discount_percentage, reverse=True)
            
            # Limita a quantidade de produtos
            products = products[:20]  # Envia no máximo 20 produtos
            
            logger.info(f"Enviando {len(products)} produtos...")
            
            # Envia email
            if self.notification_manager.send_email(products):
                logger.info("Email enviado com sucesso!")
            
            # Envia WhatsApp (apenas os 5 melhores)
            top_products = products[:5]
            if self.notification_manager.send_whatsapp_messages(top_products):
                logger.info("Mensagens WhatsApp agendadas com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro no ciclo de envio: {e}")
    
    def start_scheduler(self):
        """Inicia o agendador automático"""
        logger.info("Iniciando sistema de agendamento...")
        
        # Agenda envios a cada hora
        schedule.every().hour.do(self.send_notifications)
        
        # Executa uma vez imediatamente (opcional)
        # self.send_notifications()
        
        self.is_running = True
        
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
        
        self.thread = threading.Thread(target=run_scheduler, daemon=True)
        self.thread.start()
        
        logger.info(f"Agendador iniciado! Próximo envio em {Config.SEND_INTERVAL_HOURS} hora(s)")
    
    def stop_scheduler(self):
        """Para o agendador"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        self.scraper.close()
        logger.info("Agendador parado")
    
    def run_once(self):
        """Executa uma única vez (para testes)"""
        logger.info("Executando busca e envio único...")
        self.send_notifications()
        self.scraper.close()