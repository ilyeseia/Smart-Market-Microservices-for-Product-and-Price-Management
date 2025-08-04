"""
اختبارات التكامل بين الخدمات
"""

import unittest
import requests
import time
from typing import Dict, Any

class IntegrationTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """إعداد الاختبارات"""
        cls.base_urls = {
            'agent': 'http://localhost:8001',
            'prix': 'http://localhost:8002',
            'produits': 'http://localhost:8003'
        }
        
        # انتظار تشغيل الخدمات
        cls.wait_for_services()
    
    @classmethod
    def wait_for_services(cls, timeout: int = 60):
        """انتظار تشغيل جميع الخدمات"""
        start_time = time.time()
        
        for service_name, url in cls.base_urls.items():
            while time.time() - start_time < timeout:
                try:
                    response = requests.get(f"{url}/health", timeout=5)
                    if response.status_code == 200:
                        print(f"✅ {service_name} service is ready")
                        break
                except requests.exceptions.RequestException:
                    time.sleep(2)
            else:
                raise Exception(f"❌ {service_name} service did not start within {timeout} seconds")
    
    def test_services_health(self):
        """اختبار صحة جميع الخدمات"""
        for service_name, url in self.base_urls.items():
            with self.subTest(service=service_name):
                response = requests.get(f"{url}/health")
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertTrue(data.get('healthy', False))
    
    def test_prix_service_integration(self):
        """اختبار تكامل خدمة الأسعار"""
        # إنشاء منتج جديد
        product_data = {
            "name": "منتج تجريبي",
            "description": "وصف المنتج التجريبي"
        }
        
        response = requests.post(
            f"{self.base_urls['produits']}/products",
            json=product_data
        )
        self.assertEqual(response.status_code, 201)
        product = response.json()
        
        # إضافة سعر للمنتج
        price_data = {
            "product_id": product['id'],
            "price": 100.50,
            "currency": "DZD"
        }
        
        response = requests.post(
            f"{self.base_urls['prix']}/prices",
            json=price_data
        )
        self.assertEqual(response.status_code, 201)
    
    def test_agent_service_integration(self):
        """اختبار تكامل خدمة الوكيل الذكي"""
        # اختبار استخراج البيانات
        extraction_data = {
            "url": "https://example.com",
            "selectors": {
                "title": "h1",
                "price": ".price"
            }
        }
        
        response = requests.post(
            f"{self.base_urls['agent']}/extract",
            json=extraction_data
        )
        self.assertIn(response.status_code, [200, 202])  # قد يكون غير متزامن
    
    def test_full_workflow(self):
        """اختبار سير العمل الكامل"""
        # 1. إنشاء منتج
        product_data = {
            "name": "منتج سير العمل",
            "description": "منتج لاختبار سير العمل الكامل"
        }
        
        response = requests.post(
            f"{self.base_urls['produits']}/products",
            json=product_data
        )
        self.assertEqual(response.status_code, 201)
        product = response.json()
        
        # 2. إضافة سعر
        price_data = {
            "product_id": product['id'],
            "price": 250.00,
            "currency": "DZD"
        }
        
        response = requests.post(
            f"{self.base_urls['prix']}/prices",
            json=price_data
        )
        self.assertEqual(response.status_code, 201)
        
        # 3. استخراج معلومات إضافية بالوكيل
        extraction_data = {
            "product_id": product['id'],
            "url": "https://example.com/product",
            "selectors": {
                "reviews": ".reviews",
                "rating": ".rating"
            }
        }
        
        response = requests.post(
            f"{self.base_urls['agent']}/extract",
            json=extraction_data
        )
        self.assertIn(response.status_code, [200, 202])

if __name__ == '__main__':
    unittest.main()
