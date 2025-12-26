from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7511755689  # SENING ADMIN ID
CHANNELS = [
    -1001234567890  # ZAYAVKA KANAL ID (keyin almashtiramiz)
]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = set()

async def check_sub(user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    users.add(msg.from_user.id)

    if msg.from_user.id == ADMIN_ID:
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("📊 Statistika", callback_data="stats"))
        await msg.answer("👑 Admin panel", reply_markup=kb)
        return

    if not await check_sub(msg.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton(
                "📥 Kanalga obuna bo‘lish",
                url="https://t.me/+INVITE_LINK"
            )
        )
        kb.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check"))
        await msg.answer("Botdan foydalanish uchun kanalga obuna bo‘ling 👇", reply_markup=kb)
    else:
        await msg.answer("🎬 Kino kodini yuboring")

@dp.callback_query_handler(text="check")
async def recheck(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.edit_text("✅ Obuna tasdiqlandi. Kino kodini yuboring")
    else:
        await call.answer("❌ Hali obuna emassiz", show_alert=True)

@dp.callback_query_handler(text="stats")
async def stats(call: types.CallbackQuery):
    await call.message.answer(
        f"📊 STATISTIKA\n\n"
        f"👥 Jami userlar: {len(users)}"
    )

executor.start_polling(dp)
