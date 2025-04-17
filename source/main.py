from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from bad_words import BAD_WORDS  # Импортируем список нежелательных слов

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Состояния для FSM
class Form(StatesGroup):
    waiting_for_caps_text = State()
    waiting_for_reverse_text = State()

# Клавиатура
def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/help")],
            [KeyboardButton(text="/caps")],
            [KeyboardButton(text="/reverse")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# /start
@dp.message(Command("start"))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь', reply_markup=get_keyboard())

# /help
@dp.message(Command("help"))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь, и я повторю его в ответ.')

# /caps
@dp.message(Command("caps"))
async def process_caps_command(message: Message, state: FSMContext):
    await message.answer("Отправь текст, который нужно ПРЕОБРАЗОВАТЬ В ВЕРХНИЙ РЕГИСТР.")
    await state.set_state(Form.waiting_for_caps_text)

@dp.message(Form.waiting_for_caps_text)
async def process_caps_text(message: Message, state: FSMContext):
    text = message.text
    if any(bad_word in text.lower() for bad_word in BAD_WORDS):
        await message.answer("Ваше сообщение содержит нежелательные слова.")
    else:
        await message.answer(text.upper())
    await state.clear()

# /reverse
@dp.message(Command("reverse"))
async def process_reverse_command(message: Message, state: FSMContext):
    await message.answer("Отправь текст, который нужно ПЕРЕВЕРНУТЬ.")
    await state.set_state(Form.waiting_for_reverse_text)

@dp.message(Form.waiting_for_reverse_text)
async def process_reverse_text(message: Message, state: FSMContext):
    text = message.text
    if any(bad_word in text.lower() for bad_word in BAD_WORDS):
        await message.answer("Ваше сообщение содержит нежелательные слова.")
    else:
        await message.answer(text[::-1])
    await state.clear()

# Фото
@dp.message(lambda message: message.photo)
async def process_photo_message(message: Message):
    await message.answer("Крутое фото!")

# Эхо-сообщения
@dp.message()
async def send_echo(message: Message):
    if any(bad_word in message.text.lower() for bad_word in BAD_WORDS):
        await message.answer("Ваше сообщение содержит нежелательные слова.")
    else:
        await message.reply(message.text)

# Запуск
if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))
