import pytest
from unittest.mock import patch, call
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pizza_code import BBQPizza, PeperoniPizza, SeaPizza, Order, Pizza


class TestPizzaClasses:

    def test_bbq_pizza_creation(self):

        pizza = BBQPizza()

        assert pizza.name == "BBQ Пицца"
        assert pizza.cost == 450
        assert "курица" in str(pizza)
        assert "барбекю" in str(pizza)

    def test_peperoni_pizza_creation(self):
        pizza = PeperoniPizza()

        assert pizza.name == "Пепперони"
        assert pizza.cost == 500
        assert "пепперони" in str(pizza)
        assert "томатный" in str(pizza)

    def test_sea_pizza_creation(self):

        pizza = SeaPizza()

        assert pizza.name == "Морская"
        assert pizza.cost == 650
        assert "креветки" in str(pizza)
        assert "сливочный" in str(pizza)

    def test_pizza_backing_methods(self):

        bbq_pizza = BBQPizza()
        peperoni_pizza = PeperoniPizza()
        sea_pizza = SeaPizza()

        assert "Готовим BBQ пиццу" in bbq_pizza.backing()
        assert "курица" in bbq_pizza.backing()

        assert "Готовим Пепперони" in peperoni_pizza.backing()
        assert "пепперони" in peperoni_pizza.backing()

        assert "Готовим Морскую пиццу" in sea_pizza.backing()
        assert "креветки" in sea_pizza.backing()

    def test_pizza_string_representation(self):

        pizza = BBQPizza()

        pizza_str = str(pizza)

        assert "BBQ Пицца" in pizza_str
        assert "толстое" in pizza_str
        assert "барбекю" in pizza_str
        assert "курица" in pizza_str
        assert "450" in pizza_str

    def test_pizza_cost_property(self):

        pizza = BBQPizza()

        assert pizza.cost == 450
        with pytest.raises(AttributeError):
            pizza.cost = 500


class TestOrderManagement:
    def test_add_pizza_to_order(self):

        order = Order()
        pizza = BBQPizza()
        order.add_pizza(pizza)

        assert len(order.pizzas) == 1
        assert order.pizzas[0].name == "BBQ Пицца"
        assert order.pizzas[0].cost == 450

    def test_remove_pizza_from_order(self):

        order = Order()
        pizza1 = BBQPizza()
        pizza2 = PeperoniPizza()
        order.add_pizza(pizza1)
        order.add_pizza(pizza2)
        removed_pizza = order.remove_pizza(0)

        assert len(order.pizzas) == 1
        assert removed_pizza.name == "BBQ Пицца"
        assert order.pizzas[0].name == "Пепперони"

    def test_remove_pizza_invalid_index(self):

        order = Order()
        pizza = BBQPizza()
        order.add_pizza(pizza)

        result = order.remove_pizza(5)  # Неверный индекс

        assert result is None
        assert len(order.pizzas) == 1

    def test_calculate_total_cost_empty_order(self):

        order = Order()

        total_cost = order.calculate_total_cost()

        assert total_cost == 0

    def test_calculate_total_cost_multiple_pizzas(self):

        order = Order()
        order.add_pizza(BBQPizza())  # 450
        order.add_pizza(PeperoniPizza())  # 500
        order.add_pizza(SeaPizza())  # 650

        total_cost = order.calculate_total_cost()

        expected_total = 450 + 500 + 650
        assert total_cost == expected_total

    def test_clear_order(self):

        order = Order()
        order.add_pizza(BBQPizza())
        order.add_pizza(PeperoniPizza())

        order.clear_order()

        assert len(order.pizzas) == 0
        assert order.calculate_total_cost() == 0

    @patch('builtins.print')
    def test_show_order_with_pizzas(self, mock_print):

        order = Order()
        order.add_pizza(BBQPizza())
        order.add_pizza(PeperoniPizza())
        order.show_order()

        assert mock_print.called
        output_text = " ".join(str(call_obj) for call_obj in mock_print.call_args_list)
        assert "BBQ Пицца" in output_text
        assert "Пепперони" in output_text
        assert "Общая стоимость" in output_text

    @patch('builtins.print')
    def test_confirm_order_with_pizzas(self, mock_print):

        order = Order()
        order.add_pizza(BBQPizza())
        order.add_pizza(PeperoniPizza())

        with patch('time.sleep'):
            order.confirm_order()

        assert mock_print.called
        output_text = " ".join(str(call_obj) for call_obj in mock_print.call_args_list)
        assert "Начинаем приготовление" in output_text
        assert "Готовим BBQ пиццу" in output_text
        assert "Готовим Пепперони" in output_text
        assert "ЗАКАЗ ГОТОВ" in output_text

    @patch('builtins.print')
    def test_confirm_empty_order(self, mock_print):

        order = Order()

        order.confirm_order()

        mock_print.assert_called_with("Заказ пуст! Добавьте пиццы.")


class TestOrderScenarios:
    def test_complete_order_flow(self):

        order = Order()
        order.add_pizza(BBQPizza())
        order.add_pizza(SeaPizza())

        assert len(order.pizzas) == 2
        assert order.calculate_total_cost() == 450 + 650

        order.remove_pizza(0)

        assert len(order.pizzas) == 1
        assert order.pizzas[0].name == "Морская"
        assert order.calculate_total_cost() == 650

    @patch('builtins.print')
    def test_show_empty_order(self, mock_print):

        order = Order()
        result = order.show_order()
        assert result == "Заказ пуст"

    def test_order_initialization(self):

        order = Order()
        assert order.pizzas == []
        assert len(order.pizzas) == 0




class TestEdgeCases:
    def test_negative_index_removal(self):

        order = Order()
        order.add_pizza(BBQPizza())

        result = order.remove_pizza(-1)

        assert result is None
        assert len(order.pizzas) == 1

    def test_multiple_operations_on_empty_order(self):

        order = Order()
        assert order.calculate_total_cost() == 0
        assert order.remove_pizza(0) is None
        order.clear_order()
        assert len(order.pizzas) == 0

    def test_remove_from_empty_order(self):

        order = Order()
        result = order.remove_pizza(0)
        assert result is None

    def test_cost_property_consistency(self):

        bbq = BBQPizza()
        peperoni = PeperoniPizza()
        sea = SeaPizza()

        assert bbq.cost == 450
        assert peperoni.cost == 500
        assert sea.cost == 650
        assert bbq.cost == 450


class TestPizzaInheritance:
    def test_pizza_is_abstract(self):
        with pytest.raises(TypeError):
            Pizza("Тест", "тест", "тест", "тест", 100)

    def test_concrete_pizzas_implement_backing(self):
        bbq = BBQPizza()
        peperoni = PeperoniPizza()
        sea = SeaPizza()

        assert bbq.backing() is not None
        assert peperoni.backing() is not None
        assert sea.backing() is not None
        assert isinstance(bbq.backing(), str)
        assert isinstance(peperoni.backing(), str)
        assert isinstance(sea.backing(), str)


class TestIntegrationScenarios:
    @patch('builtins.print')
    def test_full_order_lifecycle(self, mock_print):
        order = Order()
        order.add_pizza(BBQPizza())
        order.add_pizza(PeperoniPizza())
        order.add_pizza(SeaPizza())

        assert len(order.pizzas) == 3
        assert order.calculate_total_cost() == 1600

        removed = order.remove_pizza(1)
        assert removed.name == "Пепперони"

        assert len(order.pizzas) == 2
        assert order.calculate_total_cost() == 1100
        order.clear_order()
        assert len(order.pizzas) == 0
        assert order.calculate_total_cost() == 0

    def test_pizza_immutability(self):
        pizza = BBQPizza()
        original_name = pizza.name
        original_cost = pizza.cost

        assert pizza.name == original_name
        assert pizza.cost == original_cost
        assert pizza.name == "BBQ Пицца"
        assert pizza.cost == 450


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=pizza_code", "--cov-report=term-missing"])