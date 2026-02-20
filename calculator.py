import math
from recipes import RECIPES, RESERVE_COEFFICIENT


def calculate_ingredients(selected_dishes: list[str], guests: int) -> dict:
    if guests <= 0:
        raise ValueError("Количество гостей должно быть больше 0")

    total_ingredients = {}

    for dish in selected_dishes:
        if dish not in RECIPES:
            raise ValueError(f"Блюдо '{dish}' отсутствует")

        for ingredient in RECIPES[dish]:
            name = ingredient["name"]
            unit = ingredient["unit"]
            per_person = ingredient["per_person"]

            amount = per_person * guests * RESERVE_COEFFICIENT

            if name not in total_ingredients:
                total_ingredients[name] = {"unit": unit, "amount": 0}

            total_ingredients[name]["amount"] += amount

    final_result = {}

    for name, data in total_ingredients.items():
        unit = data["unit"]
        amount = data["amount"]

        if unit == "g":
            kg = amount / 1000
            final_result[name] = f"{round(kg, 1)} кг"

        elif unit == "pcs":
            final_result[name] = f"{math.ceil(amount)} шт"

        else:
            final_result[name] = f"{amount}"

    return final_result