# مشروع الخدمات المتعددة (Microservices Project)

## نظرة عامة
هذا المشروع يحتوي على عدة خدمات مترابطة:
- **agent-intelligent**: خدمة الوكيل الذكي لاستخراج البيانات
- **prix-service**: خدمة إدارة الأسعار
- **produits-service**: خدمة إدارة المنتجات

## الهيكل العام للمشروع
```
developper/
├── agent-intelligent/          # خدمة الوكيل الذكي
├── prix-service/              # خدمة الأسعار
├── produits-service/          # خدمة المنتجات
├── shared/                    # الملفات المشتركة
│   ├── common/               # المكتبات والأدوات المشتركة
│   └── config/               # إعدادات مشتركة
├── docs/                     # الوثائق
├── tests/                    # اختبارات المشروع
│   └── integration/          # اختبارات التكامل
├── scripts/                  # سكريبتات التشغيل والإدارة
└── deployment/               # ملفات النشر
```

## كيفية التشغيل
1. تأكد من تثبيت Docker و Docker Compose
2. شغل الأمر: `docker-compose up`
3. الخدمات ستكون متاحة على:
   - Agent Service: http://localhost:8001
   - Prix Service: http://localhost:8002
   - Produits Service: http://localhost:8003

## المساهمة
يرجى قراءة دليل المساهمة في مجلد `docs/`

## الترخيص
keskasilyes@gmail.com
