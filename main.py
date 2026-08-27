import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    BusinessMessagesDeleted
)

# -------------------------------------------------------------
# 1. ТОКЕН БОТА
# -------------------------------------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8823371024:AAE8Eh_8hXkZByxJGVAqHmZng6JNcPo_YdA")
BOT_USERNAME = "@Ai_dialoog_bot"  # Юзернейм твоего бота

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище сообщений в памяти для отслеживания удалений/изменений
# В продакшене лучше использовать БД, но для старта достаточно словаря
messages_db = {}

# -------------------------------------------------------------
# 2. КОМАНДА /start И ИНЛАЙН-КНОПКИ
# -------------------------------------------------------------
@dp.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "🚀 **Добро пожаловать!**\n\n"
        "🤖 **Бот полностью бесплатный и готов к работе.**\n\n"
        "🔥 **Возможности бота**\n"
        "🗑 Отслеживание удалённых сообщений\n"
        "✏️ Отслеживание изменённых сообщений\n"
        "📸 Сохранение одноразовых сообщений\n"
        "🎥 Поддержка кружков, видео и фотографий\n"
        "🆕 Уникальные функции и команды\n\n"
        "❓ **Как подключить бота**\n"
        "1. Нажмите кнопку «📋 Скопировать».\n"
        "2. Нажмите кнопку «🔗 Подключить».\n"
        "3. Выберите **[:] Автоматизация чатов**.\n"
        "4. Вставьте текст, который был скопирован после нажатия кнопки «📋 Скопировать»."
    )

    # Кнопки как на скриншоте
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Скопировать", callback_data="copy_username"),
            InlineKeyboardButton(text="🔗 Подключить", url="tg://settings/business/bots")
        ]
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

# Обработка кнопки "Скопировать"
@dp.callback_query(F.data == "copy_username")
async def copy_callback(query: CallbackQuery):
    await query.answer(f"Скопировано: {BOT_USERNAME}", show_alert=True)
    await query.message.answer(f"`{BOT_USERNAME}`", parse_mode="Markdown")

# -------------------------------------------------------------
# 3. TELEGRAM BUSINESS: ОБРАБОТКА И СОХРАНЕНИЕ СООБЩЕНИЙ
# -------------------------------------------------------------

# Новые сообщения из бизнес-чатов
@dp.business_message()
async def handle_business_message(message: Message):
    # Сохраняем сообщение в локальный кэш
    messages_db[message.message_id] = {
        "text": message.text or message.caption or "[Медиафайл]",
        "from_user": message.from_user.full_name if message.from_user else "Собеседник",
        "chat_id": message.chat.id
    }

    # Если прислали одноразовое фото/видео (TTL), пересылаем владельцу в ЛС бота
    if message.has_protected_content or getattr(message, "ttl_seconds", None):
        try:
            await bot.send_message(
                chat_id=message.business_connection_id, # Владельцу бизнес-аккаунта
                text=f"📸 **Перехвачено одноразовое медиа/сообщение от {message.from_user.full_name}!**"
            )
            await message.forward(chat_id=message.business_connection_id)
        except Exception:
            pass

# Изменённые сообщения в бизнес-чатах
@dp.edited_business_message()
async def handle_edited_business_message(message: Message):
    old_data = messages_db.get(message.message_id)
    old_text = old_data["text"] if old_data else "Неизвестно"
    new_text = message.text or message.caption or "[Новое медиа]"

    # Обновляем сохраненный текст
    if message.message_id in messages_db:
        messages_db[message.message_id]["text"] = new_text

    notify_text = (
        f"✏️ **Сообщение было изменено!**\n"
        f"👤 **От:** {message.from_user.full_name}\n\n"
        f"❌ **Было:** {old_text}\n"
        f"✅ **Стало:** {new_text}"
    )
    
    # Отправляем уведомление владельцу
    try:
        await bot.send_message(chat_id=message.from_user.id, text=notify_text, parse_mode="Markdown")
    except Exception:
        pass

# Удалённые сообщения в бизнес-чатах
@dp.business_messages_deleted()
async def handle_deleted_business_messages(business_messages: BusinessMessagesDeleted):
    for msg_id in business_messages.message_ids:
        deleted_data = messages_db.pop(msg_id, None)
        if deleted_data:
            notify_text = (
                f"🗑 **Сообщение было удалено!**\n"
                f"👤 **Автор:** {deleted_data['from_user']}\n"
                f"💬 **Текст:** {deleted_data['text']}"
            )
            try:
                # Отправляем инфо в чат
                await bot.send_message(chat_id=business_messages.chat.id, text=notify_text, parse_mode="Markdown")
            except Exception:
                pass

# -------------------------------------------------------------
# 4. ФЕЙКОВЫЙ ВЕБ-СЕРВЕР ДЛЯ РЕНДЕРА (ДЛЯ КРУГЛОСУТОЧНОЙ РАБОТЫ)
# -------------------------------------------------------------
async def handle_ping(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# -------------------------------------------------------------
# 5. ГЛАВНЫЙ ЗАПУСК
# -------------------------------------------------------------
async def main():
    await start_web_server()
    print("🚀 Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

