UML-Style Class Diagram (Plain Text)

Class: Account
Attributes:
- accountId: String
- name: String
- purchaseHistory: List<Transaction>
Methods:
- verifyRealUser(): Boolean
- addTransaction(tx: Transaction): Void
- getPurchaseHistory(): List<Transaction>

Class: Menu
Attributes:
- items: List<MenuItem>
Methods:
- addItem(item: MenuItem): Void
- removeItem(itemId: String): Void
- getAllItems(): List<MenuItem>
- filterByCategory(category: String): List<MenuItem>

Class: Transaction
Attributes:
- transactionId: String
- selectedItems: List<MenuItem>
- totalCost: Decimal
- createdAt: DateTime
Methods:
- addItem(item: MenuItem): Void
- removeItem(itemId: String): Void
- calculateTotalCost(): Decimal

Class: MenuItem
Attributes:
- itemId: String
- name: String
- price: Decimal
- category: String
- popularityRating: Float
Methods:
- isInCategory(category: String): Boolean

Associations and Multiplicity:
- Account 1 ---- 0..* Transaction
- Menu 1 ---- 0..* MenuItem
- Transaction 1 ---- 1..* MenuItem