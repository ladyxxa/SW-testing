import time
from abc import ABC, abstractmethod


class Pizza(ABC):
    """Базовый класс для всех пицц"""

    def __init__(self, name, topping, sauce, crust, cost):
        self.name = name
        self._topping = topping
        self._sauce = sauce
        self._crust = crust
        self._cost = cost

    @abstractmethod
    def backing(self):
        pass

    def __str__(self):
        return f"{self.name}: {self._crust} тесто, соус {self._sauce}, начинка: {self._topping} - {self._cost} руб."

    @property
    def cost(self):
        return self._cost


class BBQPizza(Pizza):
    def __init__(self):
        super().__init__("BBQ Пицца", "курица", "барбекю", "толстое", 450)

    def backing(self):
        return f"Готовим BBQ пиццу: {self._crust} тесто, соус {self._sauce}, начинка {self._topping}"


class PeperoniPizza(Pizza):
    def __init__(self):
        super().__init__("Пепперони", "пепперони", "томатный", "тонкое", 500)

    def backing(self):
        return f"Готовим Пепперони: {self._crust} тесто, соус {self._sauce}, начинка {self._topping}"


class SeaPizza(Pizza):
    def __init__(self):
        super().__init__("Морская", "креветки, морепродукты", "сливочный", "тонкое", 650)

    def backing(self):
        return f"Готовим Морскую пиццу: {self._crust} тесто, соус {self._sauce}, начинка {self._topping}"


class Order:
    """Класс для управления заказом"""

    def __init__(self):
        self.pizzas = []

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)
        print(f"Пицца '{pizza.name}' добавлена в заказ!")

    def remove_pizza(self, index):
        if 0 <= index < len(self.pizzas):
            removed_pizza = self.pizzas.pop(index)
            print(f"Пицца '{removed_pizza.name}' удалена из заказа!")
            return removed_pizza
        else:
            print("Неверный номер пиццы!")
            return None

    def calculate_total_cost(self):
        return sum(pizza.cost for pizza in self.pizzas)

    def show_order(self):
        if not self.pizzas:
            return "Заказ пуст"

        print("\n" + "=" * 50)
        print("ВАШ ЗАКАЗ:")
        print("=" * 50)
        for i, pizza in enumerate(self.pizzas, 1):
            print(f"{i}. {pizza}")
        print(f"\nОбщая стоимость: {self.calculate_total_cost()} руб.")
        print("=" * 50)

    def confirm_order(self):
        if not self.pizzas:
            print("Заказ пуст! Добавьте пиццы.")
            return

        print("\nНачинаем приготовление заказа...")
        for i, pizza in enumerate(self.pizzas, 1):
            print(f"{i}. {pizza.backing()}")
            time.sleep(2)


        print("ЗАКАЗ ГОТОВ! ПРИЯТНОГО АППЕТИТА!")

    def clear_order(self):
        self.pizzas.clear()
        print("Заказ очищен!")


def main():
    """Главная функция программы"""
    order = Order()

    pizza_types = {
        '1': BBQPizza,
        '2': PeperoniPizza,
        '3': SeaPizza
    }

    while True:
        print("\n" + "=" * 50)
        print("ПИЦЦЕРИЯ - МЕНЮ")
        print("=" * 50)
        print("1. Посмотреть заказ")
        print("2. Добавить пиццу")
        print("3. Удалить пиццу")
        print("4. Подтвердить заказ")
        print("5. Очистить заказ")
        print("6. Выйти")
        print("=" * 50)

        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            order.show_order()

        elif choice == '2':
            print("\nДоступные пиццы:")
            print("1. BBQ Пицца (450 руб.) - курица, соус барбекю, толстое тесто")
            print("2. Пепперони (500 руб.) - пепперони, томатный соус, тонкое тесто")
            print("3. Морская (650 руб.) - креветки, морепродукты, сливочный соус, тонкое тесто")

            pizza_choice = input("Выберите пиццу (1-3): ").strip()

            if pizza_choice in pizza_types:
                pizza = pizza_types[pizza_choice]()
                order.add_pizza(pizza)
            else:
                print("Неверный выбор пиццы!")

        elif choice == '3':
            if not order.pizzas:
                print("Заказ пуст! Нечего удалять.")
                continue

            order.show_order()
            try:
                index = int(input("Введите номер пиццы для удаления: ")) - 1
                order.remove_pizza(index)
            except ValueError:
                print("Введите корректный номер!")

        elif choice == '4':
            order.confirm_order()

        elif choice == '5':
            if order.pizzas:
                confirm = input("Вы уверены, что хотите очистить заказ? (да/нет): ").lower()
                if confirm == 'да':
                    order.clear_order()
            else:
                print("Заказ уже пуст!")

        elif choice == '6':
            print("Спасибо за заказ! До свидания!")
            break

        else:
            print("Неверный выбор! Введите число от 1 до 6.")


if __name__ == "__main__":
    main()