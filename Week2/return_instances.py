class Item:
    pay_rate = 0.8
    all = []
    def __init__(self, name: str, price: float, quantity: int):
        #validations
        assert price >= 0, f"Price {price} is not valid"
        assert quantity >= 0, f"Quantity {quantity} is not valid"

        self.name = name
        self.price = price
        self.quantity = quantity

        Item.all.append(self)

    def calculate_total_price(self):
        return self.price * self.quantity
    
    def apply_discount(self):
        self.price = self.price * Item.pay_rate

    def __repr__(self):
        return f"Item('{self.name}', {self.price}, {self.quantity})"

item1 = Item("Phone", 1000, 5)
item2 = Item("Laptop", 5000, 3)
item3 = Item("Cable", 10, 50)
item4 = Item("Mouse", 20, 100)
item5 = Item("Keyboard", 50, 20)

print(Item.all)