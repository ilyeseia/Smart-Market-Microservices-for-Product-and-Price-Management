#!/bin/bash

# Ø³ÙƒØ±ÙŠØ¨Øª Ù„ØªØ´ØºÙŠÙ„ Ø¬Ù…ÙŠØ¹ Ø§Ù„Ø®Ø¯Ù…Ø§Øª

echo "ðŸš€ Ø¨Ø¯Ø¡ ØªØ´ØºÙŠÙ„ Ø¬Ù…ÙŠØ¹ Ø§Ù„Ø®Ø¯Ù…Ø§Øª..."

# Ø§Ù„ØªØ­Ù‚Ù‚ Ù…Ù† ÙˆØ¬ÙˆØ¯ Docker
if ! command -v docker &> /dev/null; then
    echo "âŒ Docker ØºÙŠØ± Ù…Ø«Ø¨Øª. ÙŠØ±Ø¬Ù‰ ØªØ«Ø¨ÙŠØª Docker Ø£ÙˆÙ„Ø§Ù‹."
    exit 1
fi

# Ø§Ù„ØªØ­Ù‚Ù‚ Ù…Ù† ÙˆØ¬ÙˆØ¯ Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "âŒ Docker Compose ØºÙŠØ± Ù…Ø«Ø¨Øª. ÙŠØ±Ø¬Ù‰ ØªØ«Ø¨ÙŠØª Docker Compose Ø£ÙˆÙ„Ø§Ù‹."
    exit 1
fi

# Ø¥Ù†Ø´Ø§Ø¡ Ø§Ù„Ø´Ø¨ÙƒØ© Ø¥Ø°Ø§ Ù„Ù… ØªÙƒÙ† Ù…ÙˆØ¬ÙˆØ¯Ø©
docker network create microservices-network 2>/dev/null || true

# ØªØ´ØºÙŠÙ„ Ø§Ù„Ø®Ø¯Ù…Ø§Øª
echo "ðŸ“¦ Ø¥Ù†Ø´Ø§Ø¡ ÙˆØªØ´ØºÙŠÙ„ Ø§Ù„Ø­Ø§ÙˆÙŠØ§Øª..."
docker-compose up --build -d

# Ø§Ù†ØªØ¸Ø§Ø± Ø­ØªÙ‰ ØªØµØ¨Ø­ Ø§Ù„Ø®Ø¯Ù…Ø§Øª Ø¬Ø§Ù‡Ø²Ø©
echo "â³ Ø§Ù†ØªØ¸Ø§Ø± ØªØ´ØºÙŠÙ„ Ø§Ù„Ø®Ø¯Ù…Ø§Øª..."
sleep 10

# ÙØ­Øµ Ø­Ø§Ù„Ø© Ø§Ù„Ø®Ø¯Ù…Ø§Øª
echo "ðŸ” ÙØ­Øµ Ø­Ø§Ù„Ø© Ø§Ù„Ø®Ø¯Ù…Ø§Øª..."
docker-compose ps

echo "âœ… ØªÙ… ØªØ´ØºÙŠÙ„ Ø¬Ù…ÙŠØ¹ Ø§Ù„Ø®Ø¯Ù…Ø§Øª Ø¨Ù†Ø¬Ø§Ø­!"
echo ""
echo "ðŸŒ Ø§Ù„Ø®Ø¯Ù…Ø§Øª Ù…ØªØ§Ø­Ø© Ø¹Ù„Ù‰:"
echo "  - Agent Service: http://localhost:8001"
echo "  - Prix Service: http://localhost:8002"
echo "  - Produits Service: http://localhost:8003"
echo ""
echo "ðŸ“Š Ù„Ù…Ø±Ø§Ù‚Ø¨Ø© Ø§Ù„Ø³Ø¬Ù„Ø§Øª: docker-compose logs -f"
echo "ðŸ›‘ Ù„Ø¥ÙŠÙ‚Ø§Ù Ø§Ù„Ø®Ø¯Ù…Ø§Øª: docker-compose down"
