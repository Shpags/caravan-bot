import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart

from states import EventForm
from keyboards import dishes_keyboard
from calculator import calculate_ingredients
from recipes import RECIPES

TOKEN = "8280724314:AAEtjVuWgPkGQkGSkWBUdStR45lzu-qcLQE"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, request_timeout=60)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(EventForm.choosing_dishes)
    await state.update_data(selected=[])

    await message.answer(
        "Добро пожаловать в систему расчёта мероприятий ресторана «Караван».\n"
        "Выберите блюда для мероприятия:",
        reply_markup=dishes_keyboard()
    )


@dp.callback_query(EventForm.choosing_dishes, F.data.startswith("dish:"))
async def dish_toggle(callback: CallbackQuery, state: FSMContext):
    dish_name = callback.data.split(":", 1)[1]

    if dish_name not in RECIPES:
        await callback.answer("Блюдо отсутствует", show_alert=True)
        return

    data = await state.get_data()
    selected = data.get("selected", [])

    if dish_name in selected:
        selected.remove(dish_name)
    else:
        selected.append(dish_name)

    await state.update_data(selected=selected)

    await callback.message.edit_reply_markup(
        reply_markup=dishes_keyboard(selected)
    )

    await callback.answer()


@dp.callback_query(EventForm.choosing_dishes, F.data == "done")
async def done_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected", [])

    if not selected:
        await callback.answer("Выберите хотя бы одно блюдо", show_alert=True)
        return

    await state.set_state(EventForm.waiting_for_guests)
    await callback.message.answer("Введите количество гостей:")
    await callback.answer()


@dp.message(EventForm.waiting_for_guests)
async def guests_handler(message: Message, state: FSMContext):
    try:
        guests = int(message.text)
        if guests <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Введите корректное число гостей")
        return

    data = await state.get_data()
    selected = data.get("selected", [])

    try:
        result = calculate_ingredients(selected, guests)
    except ValueError as e:
        await message.answer(str(e))
        return

    output = "\n".join(
        f"{name} – {value}" for name, value in result.items()
    )

    await message.answer(output)
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())