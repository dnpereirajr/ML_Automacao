from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Product:
    title: str
    original_price: float
    current_price: float
    discount_percentage: float
    payment_options: str
    shipping_info: str
    feedback_score: str
    product_url: str
    affiliate_url: str
    category: str
    is_promotion: bool
    image_url: Optional[str] = None
    seller_name: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def savings(self) -> float:
        return self.original_price - self.current_price
    
    def format_message(self) -> str:
        """Formata o produto no template solicitado"""
        return f"""<b>{self.title}</b>
De <s>R$ {self.original_price:.2f}</s>
Por <b>R$ {self.current_price:.2f}</b>
{self.payment_options}
{self.shipping_info}
{self.feedback_score}
📲 LINK DE COMPRA ⬇️
{self.affiliate_url}"""

@dataclass
class SearchResult:
    products: List[Product]
    total_found: int
    search_term: str
    category: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()