from decimal import Decimal

import pytest

import models
from models import Account, Menu, MenuItem, Transaction


@pytest.fixture(autouse=True)
def reset_model_id_counters() -> None:
	"""Keep tests deterministic by resetting module-level counters."""
	models._menu_item_id_counter = 0
	models._menu_id_counter = 0
	models._transaction_id_counter = 0
	models._account_id_counter = 0


def _build_sample_menu() -> Menu:
	menu = Menu()
	menu.add_item(MenuItem("Cola", Decimal("2.50"), "Drinks", 4.3))
	menu.add_item(MenuItem("Cake", Decimal("4.00"), "Desserts", 4.7))
	menu.add_item(MenuItem("Tea", Decimal("1.75"), "Drinks", 4.1))
	return menu


def test_filter_by_category_exact_match() -> None:
	menu = _build_sample_menu()

	drinks = menu.filter_by_category("Drinks")

	assert len(drinks) == 2
	assert [item.name for item in drinks] == ["Cola", "Tea"]


def test_filter_by_category_returns_empty_for_nonexistent() -> None:
	menu = _build_sample_menu()

	mains = menu.filter_by_category("Mains")

	assert mains == []


def test_filter_by_category_is_currently_case_sensitive() -> None:
	menu = _build_sample_menu()

	lower_case = menu.filter_by_category("drinks")

	# Desired behavior is case-insensitive, but current model is exact-match.
	assert lower_case == []


def test_menuitem_is_in_category_exact_match() -> None:
	item = MenuItem("Lemonade", Decimal("3.00"), "Drinks", 4.2)

	assert item.is_in_category("Drinks") is True
	assert item.is_in_category("drinks") is False


def test_calculate_total_cost_single_item() -> None:
	tx = Transaction()
	tx.add_item(MenuItem("Cookie", Decimal("1.25"), "Desserts", 4.0))

	total = tx.calculate_total_cost()

	assert total == Decimal("1.25")
	assert tx.total_cost == Decimal("1.25")


def test_calculate_total_cost_multiple_items() -> None:
	tx = Transaction()
	tx.add_item(MenuItem("Cola", Decimal("2.00"), "Drinks", 4.0))
	tx.add_item(MenuItem("Cake", Decimal("3.50"), "Desserts", 4.2))
	tx.add_item(MenuItem("Tea", Decimal("4.00"), "Drinks", 4.5))

	total = tx.calculate_total_cost()

	assert total == Decimal("9.50")


def test_calculate_total_cost_decimal_precision() -> None:
	tx = Transaction()
	tx.add_item(MenuItem("Item A", Decimal("1.99"), "Snacks", 4.0))
	tx.add_item(MenuItem("Item B", Decimal("2.01"), "Snacks", 4.0))
	tx.add_item(MenuItem("Item C", Decimal("0.50"), "Snacks", 4.0))

	assert tx.calculate_total_cost() == Decimal("4.50")


def test_calculate_total_cost_empty_transaction_is_zero() -> None:
	tx = Transaction()

	assert tx.calculate_total_cost() == Decimal("0.00")
	assert tx.total_cost == Decimal("0.00")


def test_calculate_total_cost_after_item_removal() -> None:
	tx = Transaction()
	cola = MenuItem("Cola", Decimal("5.00"), "Drinks", 4.0)
	tea = MenuItem("Tea", Decimal("5.00"), "Drinks", 4.0)
	cake = MenuItem("Cake", Decimal("5.00"), "Desserts", 4.0)
	tx.add_item(cola)
	tx.add_item(tea)
	tx.add_item(cake)

	assert tx.calculate_total_cost() == Decimal("15.00")

	tx.remove_item(tea.item_id)

	assert tx.calculate_total_cost() == Decimal("10.00")


def test_menu_add_remove_and_get_all_items_returns_copy() -> None:
	menu = Menu()
	cola = MenuItem("Cola", Decimal("2.50"), "Drinks", 4.3)
	cake = MenuItem("Cake", Decimal("4.00"), "Desserts", 4.7)
	menu.add_item(cola)
	menu.add_item(cake)

	snapshot = menu.get_all_items()
	snapshot.pop()

	assert len(menu.items) == 2

	menu.remove_item(cola.item_id)
	assert [item.name for item in menu.items] == ["Cake"]


def test_account_verify_real_user_and_purchase_history() -> None:
	account = Account("Ada")
	tx = Transaction()

	assert account.verify_real_user() is True

	account.add_transaction(tx)
	history = account.get_purchase_history()
	assert history == [tx]

	history.clear()
	assert account.get_purchase_history() == [tx]


def test_account_verify_real_user_rejects_blank_name() -> None:
	account = Account("   ")

	assert account.verify_real_user() is False


def test_ids_increment_sequentially_within_each_model() -> None:
	item1 = MenuItem("A", Decimal("1.00"), "Cat", 4.0)
	item2 = MenuItem("B", Decimal("1.00"), "Cat", 4.0)
	menu1 = Menu()
	menu2 = Menu()
	tx1 = Transaction()
	tx2 = Transaction()
	acc1 = Account("One")
	acc2 = Account("Two")

	assert item1.item_id == "1"
	assert item2.item_id == "2"
	assert menu1.menu_id == "1"
	assert menu2.menu_id == "2"
	assert tx1.transaction_id == "1"
	assert tx2.transaction_id == "2"
	assert acc1.account_id == "1"
	assert acc2.account_id == "2"

