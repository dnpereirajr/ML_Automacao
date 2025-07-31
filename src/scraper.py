import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Optional
from urllib.parse import urljoin, quote
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from .models import Product, SearchResult
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MercadoLivreScraper:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.base_url = "https://www.mercadolivre.com.br"
        self.setup_session()
    
    def setup_session(self):
        """Configura headers para parecer um navegador real"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def setup_driver(self):
        """Configura o Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            return True
        except Exception as e:
            logger.error(f"Erro ao configurar WebDriver: {e}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        """Faz login no Mercado Livre"""
        try:
            if not self.driver:
                if not self.setup_driver():
                    return False
            
            self.driver.get(f"{self.base_url}/jms/lgz/login")
            
            # Aguarda e preenche email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "user_id"))
            )
            email_input.send_keys(email)
            
            # Clica em continuar
            continue_btn = self.driver.find_element(By.CLASS_NAME, "andes-button--large")
            continue_btn.click()
            
            # Aguarda e preenche senha
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_input.send_keys(password)
            
            # Clica em entrar
            login_btn = self.driver.find_element(By.ID, "action-login-btn")
            login_btn.click()
            
            # Verifica se login foi bem-sucedido
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nav-menu-user"))
            )
            
            logger.info("Login realizado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro no login: {e}")
            return False
    
    def search_products(self, query: str, is_promotion: bool = False) -> SearchResult:
        """Busca produtos no Mercado Livre"""
        try:
            # Constrói URL de busca
            search_url = f"{self.base_url}/jm/search"
            params = {'q': query}
            
            if is_promotion:
                params['discount'] = '5-100'  # Desconto de 5% a 100%
            
            response = self.session.get(search_url, params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            products = self._parse_products(soup, query, is_promotion)
            
            return SearchResult(
                products=products,
                total_found=len(products),
                search_term=query,
                category=self._classify_category(query)
            )
            
        except Exception as e:
            logger.error(f"Erro na busca de produtos: {e}")
            return SearchResult(products=[], total_found=0, search_term=query, category="outros")
    
    def _parse_products(self, soup: BeautifulSoup, query: str, is_promotion: bool) -> List[Product]:
        """Extrai informações dos produtos da página"""
        products = []
        
        # Seleciona containers de produtos
        product_containers = soup.find_all('div', class_='ui-search-result__wrapper')
        
        for container in product_containers[:Config.MAX_PRODUCTS_PER_SEARCH]:
            try:
                product = self._extract_product_info(container, query, is_promotion)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Erro ao extrair produto: {e}")
                continue
        
        return products
    
    def _extract_product_info(self, container, query: str, is_promotion: bool) -> Optional[Product]:
        """Extrai informações de um produto específico"""
        try:
            # Título
            title_element = container.find('h2', class_='ui-search-item__title')
            if not title_element:
                return None
            title = title_element.get_text(strip=True)
            
            # Preços
            price_element = container.find('span', class_='andes-money-amount__fraction')
            if not price_element:
                return None
            current_price = float(price_element.get_text(strip=True).replace('.', '').replace(',', '.'))
            
            # Preço original (se houver desconto)
            original_price_element = container.find('s', class_='andes-money-amount--previous')
            original_price = current_price
            if original_price_element:
                original_price_text = original_price_element.find('span', class_='andes-money-amount__fraction')
                if original_price_text:
                    original_price = float(original_price_text.get_text(strip=True).replace('.', '').replace(',', '.'))
            
            # Desconto
            discount = 0
            if original_price > current_price:
                discount = ((original_price - current_price) / original_price) * 100
            
            # Link do produto
            link_element = container.find('a', class_='ui-search-link')
            product_url = link_element['href'] if link_element else ""
            
            # Informações adicionais
            shipping_info = self._extract_shipping_info(container)
            payment_options = self._extract_payment_options(container)
            feedback = self._extract_feedback(container)
            
            # Gera link de afiliado
            affiliate_url = self._generate_affiliate_link(product_url)
            
            return Product(
                title=title,
                original_price=original_price,
                current_price=current_price,
                discount_percentage=discount,
                payment_options=payment_options,
                shipping_info=shipping_info,
                feedback_score=feedback,
                product_url=product_url,
                affiliate_url=affiliate_url,
                category=self._classify_category(query),
                is_promotion=is_promotion
            )
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações do produto: {e}")
            return None
    
    def _extract_shipping_info(self, container) -> str:
        """Extrai informações de frete"""
        shipping_element = container.find('p', class_='ui-search-item__shipping')
        if shipping_element:
            return shipping_element.get_text(strip=True)
        return "Frete a calcular"
    
    def _extract_payment_options(self, container) -> str:
        """Extrai opções de pagamento"""
        installment_element = container.find('span', class_='ui-search-installments')
        if installment_element:
            return installment_element.get_text(strip=True)
        return "À vista ou parcelado"
    
    def _extract_feedback(self, container) -> str:
        """Extrai informações de feedback/avaliação"""
        rating_element = container.find('span', class_='ui-search-reviews__rating-number')
        if rating_element:
            return f"⭐ {rating_element.get_text(strip=True)}"
        return "Sem avaliações"
    
    def _generate_affiliate_link(self, product_url: str) -> str:
        """Gera link de afiliado"""
        if Config.AFFILIATE_ID and product_url:
            separator = '&' if '?' in product_url else '?'
            return f"{product_url}{separator}affiliateId={Config.AFFILIATE_ID}"
        return product_url
    
    def _classify_category(self, query: str) -> str:
        """Classifica o produto em categoria básica"""
        query_lower = query.lower()
        
        for category, keywords in Config.CATEGORIES.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return "outros"
    
    def close(self):
        """Fecha o driver do Selenium"""
        if self.driver:
            self.driver.quit()
    
    def __del__(self):
        self.close()