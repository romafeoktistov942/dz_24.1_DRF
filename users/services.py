import stripe


# from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создает продукт на страйпе"""
    return stripe.Product.create(name=product.course_name)


# def convert_rub_to_usd(amount):
#     """ Конвертирует рубли в доллары по текущему курсы """
#     print(1)
#     c = CurrencyRates()
#     print(2)
#     rate = c.get_rate('RUB', 'USD')
#     print(3)
#     return int(amount * rate)


def create_stripe_price(amount, product):
    """Функция для создания цены в Stripe"""
    return stripe.Price.create(
        currency="usd", unit_amount=amount * 100, product=product.id
    )


def create_stripe_session(product, price):
    """Создание сессии на страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
        metadata={"product_id": product.id},
    )
    return session.get("id"), session.get("url")
