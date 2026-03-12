from decimal import Decimal
from datetime import datetime
from typing import List


# Module-level ID counters for sequential ID generation
_menu_item_id_counter = 0
_menu_id_counter = 0
_transaction_id_counter = 0
_account_id_counter = 0


def _get_next_menu_item_id() -> str:
    global _menu_item_id_counter
    _menu_item_id_counter += 1
    return str(_menu_item_id_counter)


def _get_next_menu_id() -> str:
    global _menu_id_counter
    _menu_id_counter += 1
    return str(_menu_id_counter)


def _get_next_transaction_id() -> str:
    global _transaction_id_counter
    _transaction_id_counter += 1
    return str(_transaction_id_counter)


def _get_next_account_id() -> str:
    global _account_id_counter
    _account_id_counter += 1
    return str(_account_id_counter)


class MenuItem:
    """Represents a single food item in the menu with pricing and metadata."""
    
    def __init__(
        self,
        name: str,
        price: Decimal,
        category: str,
        popularity_rating: float
    ) -> None:
        """
        Initialize a MenuItem with auto-generated ID.
        
        Args:
            name: Name of the menu item
            price: Price in Decimal for financial accuracy
            category: Category of the item (e.g., 'Drinks', 'Desserts')
            popularity_rating: Float rating representing item popularity
        """
        self.item_id: str = _get_next_menu_item_id()
        self.name: str = name
        self.price: Decimal = price
        self.category: str = category
        self.popularity_rating: float = popularity_rating
    
    def is_in_category(self, category: str) -> bool:
        """
        Check if this item belongs to the specified category.
        
        Args:
            category: Category name to check against
            
        Returns:
            True if item is in the category, False otherwise
        """
        return self.category == category


class Menu:
    """Manages a collection of MenuItem objects with filtering capabilities."""
    
    def __init__(self) -> None:
        """Initialize a Menu with auto-generated ID and empty items list."""
        self.menu_id: str = _get_next_menu_id()
        self.items: List[MenuItem] = []
    
    def add_item(self, item: MenuItem) -> None:
        """
        Add a MenuItem to the menu.
        
        Args:
            item: MenuItem to add
        """
        self.items.append(item)
    
    def remove_item(self, item_id: str) -> None:
        """
        Remove a MenuItem by its ID.
        
        Args:
            item_id: ID of the item to remove
        """
        self.items = [item for item in self.items if item.item_id != item_id]
    
    def get_all_items(self) -> List[MenuItem]:
        """
        Get all items in the menu.
        
        Returns:
            List of all MenuItem objects
        """
        return self.items.copy()
    
    def filter_by_category(self, category: str) -> List[MenuItem]:
        """
        Filter menu items by category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of MenuItem objects in the specified category
        """
        return [item for item in self.items if item.is_in_category(category)]


class Transaction:
    """Represents a single purchase transaction with items and total cost."""
    
    def __init__(self) -> None:
        """Initialize a Transaction with auto-generated ID and current timestamp."""
        self.transaction_id: str = _get_next_transaction_id()
        self.selected_items: List[MenuItem] = []
        self.total_cost: Decimal = Decimal("0.00")
        self.created_at: datetime = datetime.now()
    
    def add_item(self, item: MenuItem) -> None:
        """
        Add a MenuItem to the transaction.
        
        Args:
            item: MenuItem to add
        """
        self.selected_items.append(item)
    
    def remove_item(self, item_id: str) -> None:
        """
        Remove a MenuItem from the transaction by its ID.
        
        Args:
            item_id: ID of the item to remove
        """
        self.selected_items = [item for item in self.selected_items if item.item_id != item_id]
    
    def calculate_total_cost(self) -> Decimal:
        """
        Calculate and update the total cost of the transaction.
        
        Returns:
            Total cost as Decimal, sum of all selected item prices
        """
        self.total_cost = sum(
            (item.price for item in self.selected_items),
            Decimal("0.00")
        )
        return self.total_cost


class Account:
    """Represents a user account with transaction history for verification."""
    
    def __init__(self, name: str) -> None:
        """
        Initialize an Account with auto-generated ID.
        
        Args:
            name: Name of the account holder
        """
        self.account_id: str = _get_next_account_id()
        self.name: str = name
        self.purchase_history: List[Transaction] = []
    
    def verify_real_user(self) -> bool:
        """
        Verify if the user is real based on account data.
        
        Returns:
            Boolean indicating if user appears to be real (default: True)
        """
        # Basic verification: account must have a name
        return bool(self.name and self.name.strip())
    
    def add_transaction(self, tx: Transaction) -> None:
        """
        Add a Transaction to the account's purchase history.
        
        Args:
            tx: Transaction to add
        """
        self.purchase_history.append(tx)
    
    def get_purchase_history(self) -> List[Transaction]:
        """
        Get the complete purchase history for this account.
        
        Returns:
            List of all Transaction objects for this account
        """
        return self.purchase_history.copy()