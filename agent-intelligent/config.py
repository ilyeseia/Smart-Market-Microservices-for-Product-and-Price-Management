"""
إعدادات الوكيل الذكي لجمع أسعار الخضار والفواكه
"""
import os
from typing import Dict, List

# إعدادات API
API_KEY = os.getenv("BROWSER_USE_API_KEY", "bu_58Y8QhRvrrKBFz4NNinNn1pAhYexch3Vb_YhlbziboQ")
BROWSER_USE_URL = "https://api.browser-use.com/browser"

# إعدادات الخدمات
PRIX_SERVICE_URL = os.getenv("PRIX_SERVICE_URL", "http://localhost:8002/prix")
PRODUITS_SERVICE_URL = os.getenv("PRODUITS_SERVICE_URL", "http://localhost:8003/produits")

# إعدادات جمع البيانات
SCRAPING_INTERVAL = int(os.getenv("SCRAPING_INTERVAL", "3600"))  # كل ساعة
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# مصادر البيانات
FACEBOOK_SOURCES = [
    "https://www.facebook.com/Magsetifel/?locale=ar_AR",
    "https://www.facebook.com/setif.market",
    "https://www.facebook.com/groups/setif.commerce",
]

# كلمات مفتاحية للبحث عن الأسعار
PRICE_KEYWORDS = [
    "دينار", "دج", "DA", "دأ", "د.ج", "وحدة", "كيلو", "كلغ", "kg",
    "سعر", "ثمن", "بيع", "شراء", "متوفر", "للبيع"
]

# أسماء الخضار والفواكه بالعربية والفرنسية
VEGETABLES_FRUITS = {
    # خضروات
    "طماطم": ["طماطم", "tomate", "tomatoes", "طماطة"],
    "بطاطس": ["بطاطس", "pomme de terre", "potatoes", "بطاطا"],
    "جزر": ["جزر", "carotte", "carrots", "جزرة"],
    "بصل": ["بصل", "oignon", "onion", "بصلة"],
    "فلفل": ["فلفل", "poivron", "pepper", "فليفلة"],
    "كوسا": ["كوسا", "courgette", "zucchini", "قرعة"],
    "باذنجان": ["باذنجان", "aubergine", "eggplant", "دنجال"],
    "خيار": ["خيار", "concombre", "cucumber", "قثاء"],
    "فجل": ["فجل", "radis", "radish"],
    "لفت": ["لفت", "navet", "turnip"],
    "سلق": ["سلق", "blette", "chard"],
    "خس": ["خس", "laitue", "lettuce"],
    "فقوس": ["فقوس", "fenouil", "fennel"],
    "بقدونس": ["بقدونس", "persil", "parsley"],
    "نعناع": ["نعناع", "menthe", "mint"],
    "كرفس": ["كرفس", "céleri", "celery"],
    
    # فواكه
    "تفاح": ["تفاح", "pomme", "apple", "تفاحة"],
    "برتقال": ["برتقال", "orange", "برتقالة"],
    "موز": ["موز", "banane", "banana"],
    "عنب": ["عنب", "raisin", "grape"],
    "فراولة": ["فراولة", "fraise", "strawberry", "توت"],
    "كيوي": ["كيوي", "kiwi"],
    "خوخ": ["خوخ", "pêche", "peach"],
    "مشمش": ["مشمش", "abricot", "apricot"],
    "كمثرى": ["كمثرى", "poire", "pear", "إجاص"],
    "رمان": ["رمان", "grenade", "pomegranate"],
    "تين": ["تين", "figue", "fig"],
    "عنب الشام": ["عنب الشام", "prune", "plum"],
    "بطيخ": ["بطيخ", "pastèque", "watermelon", "حبحب"],
    "شمام": ["شمام", "melon", "cantaloup"],
    "ليمون": ["ليمون", "citron", "lemon", "حامض"],
    "يوسفي": ["يوسفي", "mandarine", "mandarin", "كلمونتين"],
}

# وحدات القياس
UNITS = {
    "كيلو": "kg",
    "كلغ": "kg", 
    "kg": "kg",
    "غرام": "g",
    "جرام": "g",
    "g": "g",
    "قطعة": "piece",
    "وحدة": "unit",
    "كيس": "bag",
    "علبة": "box",
    "صندوق": "crate"
}

# إعدادات التصفية
MIN_PRICE = 10    # أقل سعر مقبول
MAX_PRICE = 2000  # أعلى سعر مقبول
