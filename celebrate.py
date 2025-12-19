from zoneinfo import ZoneInfo
import asyncio
from datetime import datetime, time, date
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
import os
from dotenv import load_dotenv

load_dotenv()

BOTTOKEN = os.getenv('BOTTOKEN')
USERID = int(os.getenv('USERID'))
MOSCOWTZ = ZoneInfo('Europe/Moscow')
BIRTHDAY = date(2025, 12, 20)

bot = Bot(BOTTOKEN)
dp = Dispatcher()

compliments = [
    "Ты всегда радуешь нас своим умом!",
    "Какая небесная улыбка!",
    "Ты - просто свет настоящий!",
]

facts = [
    "Человек значительно осмыслимее других животных",
    "На земле около 8 миллионов видов живых организмов",
    "Музыка красива, как никогда!",
]

class UserState:
    complimentindex = 0
    factindex = 0
    finished = False

userstate = UserState()

def keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😊 Комплимент", callback_data="compliment")],
        [InlineKeyboardButton(text="📚 Факт", callback_data="fact")],
    ])

@dp.message(CommandStart())
async def start(message: Message):
    today = datetime.now(MOSCOWTZ).date()
    if today == BIRTHDAY:
        await message.answer("🎉 С ДНЕМ РОЖДЕНИЯ!!!", reply_markup=keyboard())
    else:
        await message.answer("Еще не твой день...")

@dp.callback_query(F.data == "compliment")
async def sendcompliment(callback):
    idx = userstate.complimentindex
    if idx < len(compliments):
        await callback.message.answer(compliments[idx])
        userstate.complimentindex += 1
    else:
        await callback.message.answer("Все комплименты закончились!")
    await checkfinish(callback)

@dp.callback_query(F.data == "fact")
async def sendfact(callback):
    idx = userstate.factindex
    if idx < len(facts):
        await callback.message.answer(f"📌 {facts[idx]}")
        userstate.factindex += 1
    else:
        await callback.message.answer("Все факты закончились!")
    await checkfinish(callback)

async def checkfinish(callback):
    if userstate.complimentindex >= len(compliments) and userstate.factindex >= len(facts):
        await callback.message.edit_reply_markup(reply_markup=None)
        userstate.finished = True

async def scheduler():
    sent = set()
    while True:
        now = datetime.now(MOSCOWTZ)
        today = now.date()
        if today == BIRTHDAY:
            current_time = now.time()
            if time(0, 0) <= current_time < time(1, 0) and "00" not in sent:
                await bot.send_message(USERID, "🌙 С полуночи - С ДНЕМ РОЖДЕНИЯ!", reply_markup=keyboard())
                sent.add("00")
            if time(8, 0) <= current_time < time(9, 0) and "08" not in sent:
                await bot.send_message(USERID, "☕ Доброе утро!", reply_markup=keyboard())
                sent.add("08")
            if time(12, 0) <= current_time < time(13, 0) and "12" not in sent:
                await bot.send_message(USERID, "🍽 Добрый день!", reply_markup=keyboard())
                sent.add("12")
            if time(21, 0) <= current_time < time(22, 0) and "21" not in sent:
                await bot.send_message(USERID, "😘 Добрый вечер!", reply_markup=keyboard())
                sent.add("21")
        await asyncio.sleep(30)

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
