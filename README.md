# SMC Telegram Agent

Маленький FastAPI-сервер для отримання сигналів з TradingView і пересилки їх у Telegram.

## Налаштування
1. Задай Environment variables:
   - BOT_TOKEN = токен з BotFather
   - CHAT_ID = @aismagent (або chat_id групи)

2. Локально:
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 10000
