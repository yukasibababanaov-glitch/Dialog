import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token="8823371024:AAE8Eh_8hXkZByxJGVAqHmZng6JNcPo_YdA")
dp = Dispatcher()
router = Router()
dp.include_router(router)

# --- Клавиатуры ---

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="🔄 Функции", callback_data="functions"), InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="✏️ Команды", callback_data="commands")],
        [InlineKeyboardButton(text="Подписка", callback_data="subscription")],
        [InlineKeyboardButton(text="👨‍💻 Поддержка", callback_data="support")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])

def get_functions_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="AFK", callback_data="func_afk")],
        [InlineKeyboardButton(text="Форматирование", callback_data="func_format")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])

def get_format_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Жирный", callback_data="fmt_bold"), InlineKeyboardButton(text="Курсив", callback_data="fmt_italic")],
        [InlineKeyboardButton(text="Зачёркнутый", callback_data="fmt_strike"), InlineKeyboardButton(text="Подчёркнутый", callback_data="fmt_underline")],
        [InlineKeyboardButton(text="Моноширинный", callback_data="fmt_mono"), InlineKeyboardButton(text="Спойлер", callback_data="fmt_spoiler")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="functions")]
    ])

# --- Обработчики команд ---

@router.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "🚀 **Never Dialog подключён!**\n\n"
        "🔥 **Теперь вам доступны**\n"
        "🗑 просмотр удалённых и изменённых сообщений\n"
        "🔄 сохранение одноразовых сообщений\n"
        "📹 отслеживание фото, видео и кружков\n"
        "🆕 все дополнительные функции и команды бота\n\n"
        "🎂 *Приятного использования!*"
    )
    await message.answer(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

# --- Обработчики Inline-кнопок ---

@router.callback_query(F.data == "main_menu")
async def menu_callback(call: CallbackQuery):
    text = (
        "🚀 **Never Dialog подключён!**\n\n"
        "🔥 **Теперь вам доступны**\n"
        "🗑 просмотр удалённых и изменённых сообщений\n"
        "🔄 сохранение одноразовых сообщений\n"
        "📹 отслеживание фото, видео и кружков\n"
        "🆕 все дополнительные функции и команды бота\n\n"
        "🎂 *Приятного использования!*"
    )
    await call.message.edit_text(text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "commands")
async def commands_callback(call: CallbackQuery):
    text = (
        "⚙️ **Команды**\n\n"
        "Отправьте команду в личные сообщения, и она будет выполнена.\n\n"
        "🔒 `.mute [минуты]` — Мут пользователя\n"
        "🔓 `.unmute` — Снять мут\n"
        "🤍 `.love` — Анимация\n"
        "🚀 `.spam [кол-во] [текст]` — Спам\n"
        "🔄 `.spek` — Искажение текста\n"
        "⭕️ `.nomute` — Обход мута\n"
        "🎯 `.zero` — Крестики-нолики\n"
        "📊 `.status` — Статистика чата\n"
        "ℹ️ `.info` — Информация\n"
        "🚀 `.troll` — Оскорбительное сообщение\n"
        "⏳ `.afk` — AFK режим\n"
        "🎲 `.flip` — Монетка\n"
        "🎯 `.rps` — Камень, ножницы, бумага\n"
        "❓ `.help` — Список команд\n"
        "🎥 `.save [ссылка]` — Скачать видео (TikTok, YT, Inst)\n"
        "📹 `.krom` — Видео в кружок\n"
        "🎙 `.voicemod` — Изменение голоса\n"
        "📚 `.niks` — Время в фамилии\n"
        "🖼 `.stik` — Стикер из фото\n"
        "📑 `.clone` — Клонировать профиль\n"
        "➕ `.gif` — Конвертер в GIF"
    )
    await call.message.edit_text(text, reply_markup=get_back_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "functions")
async def functions_callback(call: CallbackQuery):
    text = "⚙️ **Функции**\n\nЗдесь вы можете настроить интерфейс под себя и сделать его более удобным и уникальным."
    await call.message.edit_text(text, reply_markup=get_functions_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "func_format")
async def format_callback(call: CallbackQuery):
    text = "✏️ **Форматирование текста**\n\nВыберите, как будет выглядеть ваш текст."
    await call.message.edit_text(text, reply_markup=get_format_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data == "profile")
async def profile_callback(call: CallbackQuery):
    await call.message.edit_text(f"👤 **Профиль**\n\nID: `{call.from_user.id}`\nИмя: {call.from_user.full_name}", reply_markup=get_back_keyboard(), parse_mode="Markdown")

@router.callback_query(F.data.in_({"stats", "subscription", "support", "func_afk"}))
async def generic_callback(call: CallbackQuery):
    await call.answer("Раздел в разработке!", show_alert=True)

# --- Обработка удаленных сообщений (Telegram Business API) ---

@router.business_messages_deleted()
async def business_messages_deleted_handler(event):
    # Логика перехвата удаленных сообщений
    pass

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

