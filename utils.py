import time
import logging

logger = logging.getLogger(__name__)

# Функция с повторными попытками отправки сообщений
async def send_message_with_retry(bot, chat_id, text, retries=5, delay=2):
    for attempt in range(retries):
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            break
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))
                continue
            else:
                raise
