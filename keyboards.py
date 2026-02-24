from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_dishes_keyboard():
    """
    Создаёт клавиатуру с выбором блюд для Telegram бота.
    Возвращает InlineKeyboardMarkup.
    """
    # Пример списка блюд
    dishes = ["Суп", "Пицца", "Салат", "Десерт"]

    # Формируем кнопки
    keyboard = [
        [InlineKeyboardButton(dish, callback_data=dish)] for dish in dishes
    ]

    # Создаём объект клавиатуры
    return InlineKeyboardMarkup(keyboard)