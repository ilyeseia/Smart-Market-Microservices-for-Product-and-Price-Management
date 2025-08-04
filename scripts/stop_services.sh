#!/bin/bash

# سكريبت لإيقاف جميع الخدمات

echo "🛑 إيقاف جميع الخدمات..."

# إيقاف الحاويات
docker-compose down

# إزالة الشبكة (اختياري)
read -p "هل تريد إزالة الشبكة؟ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker network rm microservices-network 2>/dev/null || true
    echo "🗑️  تم إزالة الشبكة"
fi

# إزالة الحاويات والصور (اختياري)
read -p "هل تريد إزالة الحاويات والصور؟ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose down --rmi all --volumes --remove-orphans
    echo "🗑️  تم إزالة الحاويات والصور"
fi

echo "✅ تم إيقاف جميع الخدمات بنجاح!"
