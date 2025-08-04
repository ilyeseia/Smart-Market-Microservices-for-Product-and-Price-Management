"""
منطق استخراج أسعار الخضار والفواكه من النصوص باستخدام الذكاء الاصطناعي
"""
import re
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
from bs4 import BeautifulSoup
import difflib

from config import (
    VEGETABLES_FRUITS, PRICE_KEYWORDS, UNITS, 
    MIN_PRICE, MAX_PRICE
)

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartPriceExtractor:
    def __init__(self):
        self.vegetables_fruits = VEGETABLES_FRUITS
        self.price_keywords = PRICE_KEYWORDS
        self.units = UNITS
        self.min_price = MIN_PRICE
        self.max_price = MAX_PRICE
        
    def clean_html(self, html: str) -> str:
        """
        تنظيف HTML واستخراج النص
        """
        if not html:
            return ""
            
        soup = BeautifulSoup(html, "html.parser")
        
        # إزالة العناصر غير المرغوبة
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        # استخراج النص
        text = soup.get_text(separator=" ", strip=True)
        
        # تنظيف النص
        text = re.sub(r'\s+', ' ', text)  # إزالة المسافات الزائدة
        text = re.sub(r'[^\w\s\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF.,()]', '', text)  # الحفاظ على العربية والأرقام
        
        return text.strip()
    
    def find_similar_product(self, text: str, threshold: float = 0.6) -> Optional[str]:
        """
        العثور على منتج مشابه باستخدام التشابه النصي
        """
        text_lower = text.lower()
        
        for product, variations in self.vegetables_fruits.items():
            for variation in variations:
                # مطابقة مباشرة
                if variation.lower() in text_lower:
                    return product
                
                # مطابقة بالتشابه
                similarity = difflib.SequenceMatcher(
                    None, variation.lower(), text_lower
                ).ratio()
                
                if similarity >= threshold:
                    return product
        
        return None
    
    def extract_price_from_text(self, text: str) -> List[Dict]:
        """
        استخراج معلومات السعر من النص
        """
        results = []
        
        # أنماط regex للبحث عن الأسعار
        price_patterns = [
            # نمط: [اسم المنتج] [السعر] [دينار/دج/DA]
            r'(\w+)\s+(\d{1,4})\s*(?:دينار|دج|DA|د\.ج|دأ)',
            
            # نمط: [اسم المنتج] ب [السعر] [دينار/دج/DA]
            r'(\w+)\s*ب\s*(\d{1,4})\s*(?:دينار|دج|DA|د\.ج|دأ)',
            
            # نمط: سعر [اسم المنتج] [السعر] [دينار/دج/DA]
            r'سعر\s+(\w+)\s+(\d{1,4})\s*(?:دينار|دج|DA|د\.ج|دأ)',
            
            # نمط: [اسم المنتج] [السعر]/[وحدة]
            r'(\w+)\s+(\d{1,4})\s*/\s*(\w+)',
            
            # نمط: [السعر] [دينار/دج/DA] [اسم المنتج]
            r'(\d{1,4})\s*(?:دينار|دج|DA|د\.ج|دأ)\s+(\w+)',
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                if len(match) == 2:
                    product_name, price_str = match
                    unit = "kg"  # الوحدة الافتراضية
                elif len(match) == 3:
                    product_name, price_str, unit = match
                else:
                    continue
                
                # التحقق من صحة السعر
                try:
                    price = float(price_str)
                    if not (self.min_price <= price <= self.max_price):
                        continue
                except ValueError:
                    continue
                
                # البحث عن المنتج المطابق
                matched_product = self.find_similar_product(product_name)
                if not matched_product:
                    continue
                
                # تحويل الوحدة
                unit_standardized = self.units.get(unit.lower(), unit)
                
                result = {
                    "produit": matched_product,
                    "produit_original": product_name,
                    "prix": price,
                    "unite": unit_standardized,
                    "source": "Facebook",
                    "date": str(date.today()),
                    "timestamp": datetime.now().isoformat(),
                    "confidence": 0.8  # مستوى الثقة
                }
                
                results.append(result)
        
        return results
    
    def extract_prices_from_posts(self, html: str) -> List[Dict]:
        """
        استخراج الأسعار من منشورات الفيسبوك
        """
        if not html:
            return []
        
        soup = BeautifulSoup(html, "html.parser")
        results = []
        
        # البحث عن المنشورات
        post_selectors = [
            "div[data-testid='post_message']",
            "div[data-ad-preview='message']",
            "div.userContent",
            "div.text_exposed_root",
            "span.text_exposed_hide",
            "div[role='article']",
            "div.story_body_container"
        ]
        
        posts = []
        for selector in post_selectors:
            posts.extend(soup.select(selector))
        
        # إذا لم نجد منشورات محددة، نبحث في جميع النصوص
        if not posts:
            posts = soup.find_all("div", string=True)
        
        logger.info(f"تم العثور على {len(posts)} منشور للتحليل")
        
        for i, post in enumerate(posts):
            try:
                # استخراج النص من المنشور
                text = post.get_text(separator=" ", strip=True)
                
                # تصفية المنشورات ذات الصلة
                if not any(keyword in text.lower() for keyword in self.price_keywords):
                    continue
                
                # استخراج الأسعار
                post_prices = self.extract_price_from_text(text)
                
                for price_info in post_prices:
                    price_info["post_id"] = i
                    price_info["post_text"] = text[:200]  # أول 200 حرف
                    results.append(price_info)
                    
            except Exception as e:
                logger.error(f"خطأ في تحليل المنشور {i}: {str(e)}")
                continue
        
        # إزالة التكرارات
        unique_results = []
        seen = set()
        
        for result in results:
            key = (result["produit"], result["prix"], result["unite"])
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        logger.info(f"تم استخراج {len(unique_results)} سعر فريد")
        return unique_results
    
    def validate_price_data(self, price_data: Dict) -> bool:
        """
        التحقق من صحة بيانات السعر
        """
        required_fields = ["produit", "prix", "unite", "source", "date"]
        
        for field in required_fields:
            if field not in price_data:
                return False
        
        # التحقق من السعر
        if not isinstance(price_data["prix"], (int, float)):
            return False
            
        if not (self.min_price <= price_data["prix"] <= self.max_price):
            return False
        
        # التحقق من المنتج
        if price_data["produit"] not in self.vegetables_fruits:
            return False
        
        return True

# دالة مساعدة للاستخدام السريع
def extract_prices_from_html(html: str) -> List[Dict]:
    """
    دالة مساعدة لاستخراج الأسعار من HTML
    """
    extractor = SmartPriceExtractor()
    return extractor.extract_prices_from_posts(html)

def extract_prices_from_text(text: str) -> List[Dict]:
    """
    دالة مساعدة لاستخراج الأسعار من النص
    """
    extractor = SmartPriceExtractor()
    return extractor.extract_price_from_text(text)
