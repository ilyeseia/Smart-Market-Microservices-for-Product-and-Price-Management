"""
ملف الإعدادات المشتركة للمشروع
"""

import os
from typing import Dict, Any

# إعدادات قاعدة البيانات
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'password'),
}

# إعدادات الخدمات
SERVICES_CONFIG = {
    'agent_intelligent': {
        'host': os.getenv('AGENT_HOST', 'localhost'),
        'port': int(os.getenv('AGENT_PORT', 8001)),
    },
    'prix_service': {
        'host': os.getenv('PRIX_HOST', 'localhost'),
        'port': int(os.getenv('PRIX_PORT', 8002)),
    },
    'produits_service': {
        'host': os.getenv('PRODUITS_HOST', 'localhost'),
        'port': int(os.getenv('PRODUITS_PORT', 8003)),
    }
}

# إعدادات Redis
REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
}

# إعدادات التسجيل
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

def get_database_url(service_name: str) -> str:
    """إرجاع رابط قاعدة البيانات لخدمة معينة"""
    return f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{service_name}_db"

def get_service_url(service_name: str) -> str:
    """إرجاع رابط الخدمة"""
    config = SERVICES_CONFIG.get(service_name)
    if not config:
        raise ValueError(f"Service {service_name} not found in configuration")
    return f"http://{config['host']}:{config['port']}"
