def calculate_price(cost: float, markup: float=0, discount: float=0) -> float:
    return round(cost * (1 + markup / 100) * (1 - discount / 100), 2)
