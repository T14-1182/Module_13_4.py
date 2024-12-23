import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Токен бота
with open("token.txt") as f:
    TOKEN = f.read().strip()

# Инициализация бота
bot = Bot(token=TOKEN)

# Все обработчики должны быть подключены к маршрутизатору (или Диспетчеру)
dp = Dispatcher()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Обработчик команды '/start'
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Этот обработчик получает сообщения с помощью команды `/start`
    """
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message(Command('Calories'))
async def set_age(message: Message, state: FSMContext) -> None:
    """
    Этот обработчик получает сообщения с помощью команды `/Calories` и начинает работу с Машиной Состояний
    """
    # Устанавливаю состояние. новые сообщения будут направляться в соответствующую функцию
await state.set_state(UserState.age)
await message.answer("Введите свой возраст:")


@dp.message(UserState.age)
async def set_age(message: Message, state: FSMContext):
    if message.text.isdigit():
        # Сохраняю ответ
        await state.update_data(age=message.text)

        # Устанавливаю состояние. новые сообщения будут направляться в соответствующую функцию
        await state.set_state(UserState.growth)
        await message.answer("Введите свой рост:")
    else:
        await message.answer('Введите число, еще раз:')


@dp.message(UserState.growth)
async def set_growth(message: Message, state: FSMContext):
    if message.text.isdigit():
        # Сохраняю ответ
        await state.update_data(growth=message.text)

        # Устанавливаю состояние. новые сообщения будут направляться в соответствующую функцию
        await state.set_state(UserState.weight)
        await message.answer("Введите свой вес:")
    else:
        await message.answer('Введите число, еще раз:')


@dp.message(UserState.weight)
async def set_weight(message: Message, state: FSMContext):
    if message.text.isdigit():
        # Сохраняю ответ
        await state.update_data(weight=message.text)

        # Сохраняю собранные данные и останавливаю Машину Состояний
        data = await state.get_data()
        await state.clear()

        result = float(data["weight"]) * 10 + float(data["growth"]) * 6.25 - float(data["age"]) * 5 + 5
        await message.answer(f'Ваша норма калорий: {result}')
    else:
        await message.answer('Введите число, еще раз:')


# Обработчик любого текстового сообщения
@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Обработчик переадресует полученное сообщение обратно отправителю
    """
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main() -> None:
    """
    Запуск Диспетчера событий
    """
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                        format='%(asctime)s | %(message)s')
    asyncio.run(main())