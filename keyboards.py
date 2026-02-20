from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from recipes import RECIPES


def dishes_keyboard(selected: list[str] | None = None):
    if selected is None:
        selected = []

    buttons = []

    for dish in RECIPES.keys():
        text = f"✅ {dish}" if dish in selected else dish
        buttons.append(
            [InlineKeyboardButton(text=text, callback_data=f"dish:{dish}")]
        )

    buttons.append(
        [InlineKeyboardButton(text="Готово", callback_data="done")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)