import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
import asyncio
import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class Database:
    def __init__(self, db_path='HELPER.db'):
        self.db_path = db_path
        self.conn = None

    async def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            await self._create_tables()
            logger.info("✅ Таблицы успешно созданы")
        except Exception as e:
            logger.error(f"❌ Ошибка при создании таблиц: {e}")

    async def _create_tables(self):
        cursor = self.conn.cursor()
        
        # Создаем таблицу users (если не существует)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создаем таблицу responses (если не существует)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_text TEXT,
                response_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        
        self.conn.commit()
        logger.info("🔄 Проверка таблиц завершена")

    async def save_response(self, user: types.User, message_text: str):
        try:
            cursor = self.conn.cursor()
            
            # Вставляем или обновляем пользователя
            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, username, full_name)
                VALUES (?, ?, ?)
            """, (user.id, user.username, user.full_name))
            
            # Вставляем ответ
            cursor.execute("""
                INSERT INTO responses (user_id, message_text)
                VALUES (?, ?)
            """, (user.id, message_text))
            
            self.conn.commit()
            logger.info(f"💾 Сообщение от {user.full_name} сохранено")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения: {e}")
            return False
        

class Database1:
    def __init__(self, db_path='DEEDBACKER.db'):
        self.db_path = db_path
        self.conn = None

    async def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            await self._create_tables()
            logger.info("✅ Таблицы успешно созданы")
        except Exception as e:
            logger.error(f"❌ Ошибка при создании таблиц: {e}")

    async def _create_tables(self):
        cursor = self.conn.cursor()
        
        # Создаем таблицу users (если не существует)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создаем таблицу responses (если не существует)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_text TEXT,
                response_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        
        self.conn.commit()
        logger.info("🔄 Проверка таблиц завершена")

    async def save_response1(self, user: types.User, message_text: str):
        try:
            cursor = self.conn.cursor()
            
            # Вставляем или обновляем пользователя
            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, username, full_name)
                VALUES (?, ?, ?)
            """, (user.id, user.username, user.full_name))
            
            # Вставляем ответ
            cursor.execute("""
                INSERT INTO responses (user_id, message_text)
                VALUES (?, ?)
            """, (user.id, message_text))
            
            self.conn.commit()
            logger.info(f"💾 Сообщение от {user.full_name} сохранено")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения: {e}")
            return False






set_comand = {
    BotCommand(command = 'help', description='Поддержка'),
    BotCommand(command = 'feedback', description='Поделись мнением')
}
# Инициализация
from config import TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher()
db = Database()  # Путь можно изменить: Database('path/to/database.db')
db1 = Database1()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я бот HR асистент")


class Form(StatesGroup):
    waiting_for_question = State()
    waiting_for_feedback = State()

@dp.message(Command("help"))
async def help_cmd(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_question)
    await message.answer("Напишите ваш вопрос:")

@dp.message(Command("feedback"))
async def feedback_cmd(message: types.Message, state: FSMContext):
    await state.set_state(Form.waiting_for_feedback)
    await message.answer("Расскажите ваше мнение:")

@dp.message(Form.waiting_for_question)
async def save_question(message: types.Message, state: FSMContext):
    await state.clear()
    if await db.save_response(message.from_user, message.text):
        await message.answer("✅ Ваш вопрос сохранен!")
    else:
        await message.answer("❌ Не удалось сохранить вопрос")

@dp.message(Form.waiting_for_feedback)
async def save_feedback(message: types.Message, state: FSMContext):
    await state.clear()
    if await db1.save_response1(message.from_user, message.text):
        await message.answer("✅ Ваше сообщение сохранено!")
    else:
        await message.answer("❌ Не удалось сохранить сообщение")















async def set_comands(bot: Bot):
    await bot.set_my_commands(set_comand)


async def main():
    await db.connect()  # Важно: сначала подключение к БД!
    await db1.connect()
    await set_comands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())