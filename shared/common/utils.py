"""
أدوات ومكتبات مشتركة بين الخدمات
"""

import logging
import requests
from typing import Dict, Any, Optional
from functools import wraps
import time

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceClient:
    """عميل للتواصل مع الخدمات الأخرى"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """طلب GET"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في طلب GET إلى {url}: {e}")
            raise
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """طلب POST"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"خطأ في طلب POST إلى {url}: {e}")
            raise

def retry(max_attempts: int = 3, delay: float = 1.0):
    """ديكوريتر لإعادة المحاولة"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"المحاولة {attempt + 1} فشلت: {e}. إعادة المحاولة...")
                        time.sleep(delay)
                    else:
                        logger.error(f"جميع المحاولات فشلت: {e}")
            raise last_exception
        return wrapper
    return decorator

class ResponseFormatter:
    """تنسيق الردود الموحد"""
    
    @staticmethod
    def success(data: Any, message: str = "تم بنجاح") -> Dict[str, Any]:
        """رد ناجح"""
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str, code: int = 500) -> Dict[str, Any]:
        """رد خطأ"""
        return {
            "success": False,
            "message": message,
            "error_code": code
        }

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> bool:
    """التحقق من الحقول المطلوبة"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise ValueError(f"الحقول المطلوبة مفقودة: {', '.join(missing_fields)}")
    return True
